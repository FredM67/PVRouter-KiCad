#!/usr/bin/env python3
"""Generate 3D STEP models for copper straps on the output stage board.

Each strap is a 1.5mm² copper wire (~1.38mm diameter) that:
1. Starts below board at J1 pin (connector lead)
2. Goes along B.Cu (bottom surface) to first REF test pad
3. Traverses PCB upward through REF hole to F.Cu
4. Goes along F.Cu (top surface) to second REF test pad
5. Traverses PCB downward through REF hole to B.Cu
6. Goes along B.Cu to Q1 triac pad, then down as lead
"""

import cadquery as cq
import math
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeSphere
from OCP.gp import gp_Pnt, gp_Dir, gp_Ax2

# Wire parameters
WIRE_AREA = 1.5  # mm²
WIRE_D = math.sqrt(4 * WIRE_AREA / math.pi)  # ~1.38mm
WIRE_R = WIRE_D / 2
BOARD_THICKNESS = 1.6  # mm
LEAD_BELOW = 3.0  # mm of wire below board (connector leads)

# Board center (from get_board_extents)
CX, CY = 82.285225, 39.368075

# Pad positions (board coordinates, Y increases downward in KiCad)
LINE_PADS = [
    (69.2658, 46.355),       # J1 pin 1
    (69.267725, 40.003075),  # REF4
    (69.267725, 33.272075),  # REF2
    (68.632725, 29.208075),  # Q1 pad 2 (A2/LINE)
]

SLINE_PADS = [
    (59.1058, 46.355),       # J1 pin 3
    (59.742725, 40.003075),  # REF3
    (61.901725, 33.272075),  # REF1
    (63.157725, 29.208075),  # Q1 pad 1 (A1/S_LINE)
]


def board_to_3d(bx, by):
    """Convert board coords to KiCad 3D coords."""
    return (bx - CX, -(by - CY))


def make_cylinder(p1, p2, radius):
    """Create a cylinder between two 3D points."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length < 0.01:
        return None
    origin = gp_Pnt(p1[0], p1[1], p1[2])
    direction = gp_Dir(dx / length, dy / length, dz / length)
    axis = gp_Ax2(origin, direction)
    return cq.Shape(BRepPrimAPI_MakeCylinder(axis, radius, length).Shape())


def make_sphere(pt, radius):
    """Create a sphere at a 3D point."""
    return cq.Shape(BRepPrimAPI_MakeSphere(gp_Pnt(pt[0], pt[1], pt[2]), radius).Shape())


def make_strap(pads):
    """Create a copper strap 3D model."""
    pts_3d = [board_to_3d(bx, by) for bx, by in pads]

    # Z levels (KiCad 3D: Z=0 is board bottom, Z=board_thickness is board top)
    z_bcu = -WIRE_R                     # wire center on B.Cu (below bottom surface)
    z_fcu = BOARD_THICKNESS + WIRE_R    # wire center on F.Cu (above top surface)

    # Build 3D path (trimmed 1mm at each end)
    END_TRIM = 1.0  # mm to trim from each end

    p0 = pts_3d[0]
    p1 = pts_3d[1]
    p2 = pts_3d[2]
    p3 = pts_3d[3]

    # Trim start: move p0 by 1mm toward p1
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    d = math.sqrt(dx * dx + dy * dy)
    p0_trimmed = (p0[0] + dx / d * END_TRIM, p0[1] + dy / d * END_TRIM)

    # Trim end: move p3 by 1mm toward p2
    dx = p2[0] - p3[0]
    dy = p2[1] - p3[1]
    d = math.sqrt(dx * dx + dy * dy)
    p3_trimmed = (p3[0] + dx / d * END_TRIM, p3[1] + dy / d * END_TRIM)

    path = []
    path.append((p0_trimmed[0], p0_trimmed[1], z_bcu))  # B.Cu near J1
    path.append((p1[0], p1[1], z_bcu))                   # B.Cu at REF (first)
    path.append((p1[0], p1[1], z_fcu))                   # F.Cu at REF (through hole)
    path.append((p2[0], p2[1], z_fcu))                   # F.Cu at REF (second)
    path.append((p2[0], p2[1], z_bcu))                   # B.Cu at REF (through hole)
    path.append((p3_trimmed[0], p3_trimmed[1], z_bcu))  # B.Cu near Q1

    # Create all segments
    solids = []
    for i in range(len(path) - 1):
        seg = make_cylinder(path[i], path[i + 1], WIRE_R)
        if seg:
            solids.append(seg)

    # Add spheres at joints for smooth transitions
    for pt in path[1:-1]:
        solids.append(make_sphere(pt, WIRE_R))

    # Fuse all
    result = solids[0]
    for s in solids[1:]:
        result = result.fuse(s)

    return cq.Workplane("XY").newObject([result])


if __name__ == "__main__":
    print(f"Wire diameter: {WIRE_D:.2f}mm")

    print("Generating LINE strap...")
    line_strap = make_strap(LINE_PADS)
    cq.exporters.export(line_strap, "../KiCad/3dmodels/CopperStrap_LINE.step")
    print("  -> KiCad/3dmodels/CopperStrap_LINE.step")

    print("Generating S/LINE strap...")
    sline_strap = make_strap(SLINE_PADS)
    cq.exporters.export(sline_strap, "../KiCad/3dmodels/CopperStrap_SLINE.step")
    print("  -> KiCad/3dmodels/CopperStrap_SLINE.step")

    print("Done!")
