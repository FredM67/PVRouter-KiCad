#!/usr/bin/env python3
"""Generate 3D STEP models and KiCad footprints for copper straps.

Each strap is a 1.5mm² copper wire (~1.38mm diameter) connecting
the Phoenix mains connector (J1) to the triac (Q1) via two
through-board solder points (replacing the REF test pads).

Each footprint has 2 real THT pads at the solder points where the
strap passes through the PCB. The strap also solders onto J1 and Q1
pads (shared with those components).

STEP model origin = footprint origin = first pad (pad 1).
"""

import cadquery as cq
import math
import uuid
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeSphere
from OCP.gp import gp_Pnt, gp_Dir, gp_Ax2

# Wire parameters
WIRE_AREA = 1.5  # mm²
WIRE_D = math.sqrt(4 * WIRE_AREA / math.pi)  # ~1.38mm
WIRE_R = WIRE_D / 2
BOARD_THICKNESS = 1.6  # mm
END_TRIM = 1.0  # mm to trim from each end

# Pad parameters (matching TestPoint_THTPad_D3.0mm_Drill1.5mm)
PAD_SIZE = 3.0  # mm
PAD_DRILL = 1.5  # mm

# Pad positions (board coordinates, Y increases downward in KiCad)
LINE_PADS = {
    "j1":   (69.2658, 46.355),       # J1 pin 1 (shared pad)
    "ref1": (69.267725, 40.003075),  # REF4 → pad 1 (origin)
    "ref2": (69.267725, 33.272075),  # REF2 → pad 2
    "q1":   (68.632725, 29.208075),  # Q1 pad 2 (shared pad)
}

SLINE_PADS = {
    "j1":   (59.1058, 46.355),       # J1 pin 3 (shared pad)
    "ref1": (59.742725, 40.003075),  # REF3 → pad 1 (origin)
    "ref2": (61.901725, 33.272075),  # REF1 → pad 2
    "q1":   (63.157725, 29.208075),  # Q1 pad 1 (shared pad)
}


def to_3d(bx, by, origin):
    """Convert board coords to local 3D coords (Y flipped for 3D)."""
    return (bx - origin[0], -(by - origin[1]))


def to_fp(bx, by, origin):
    """Convert board coords to footprint-local coords (no Y flip)."""
    return (bx - origin[0], by - origin[1])


def make_cylinder(p1, p2, radius):
    dx, dy, dz = p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]
    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length < 0.01:
        return None
    origin = gp_Pnt(p1[0], p1[1], p1[2])
    direction = gp_Dir(dx / length, dy / length, dz / length)
    axis = gp_Ax2(origin, direction)
    return cq.Shape(BRepPrimAPI_MakeCylinder(axis, radius, length).Shape())


def make_sphere(pt, radius):
    return cq.Shape(BRepPrimAPI_MakeSphere(gp_Pnt(pt[0], pt[1], pt[2]), radius).Shape())


def trim_point(start, end, trim_mm):
    """Move start point toward end by trim_mm."""
    dx, dy = end[0] - start[0], end[1] - start[1]
    d = math.sqrt(dx * dx + dy * dy)
    return (start[0] + dx / d * trim_mm, start[1] + dy / d * trim_mm)


def make_strap_step(pads):
    """Create 3D STEP model with origin at ref1."""
    origin = pads["ref1"]
    j1 = to_3d(*pads["j1"], origin)
    r1 = to_3d(*pads["ref1"], origin)  # (0, 0)
    r2 = to_3d(*pads["ref2"], origin)
    q1 = to_3d(*pads["q1"], origin)

    z_bcu = -WIRE_R
    z_fcu = BOARD_THICKNESS + WIRE_R

    j1_t = trim_point(j1, r1, END_TRIM)
    q1_t = trim_point(q1, r2, END_TRIM)

    path = [
        (j1_t[0], j1_t[1], z_bcu),
        (r1[0], r1[1], z_bcu),
        (r1[0], r1[1], z_fcu),
        (r2[0], r2[1], z_fcu),
        (r2[0], r2[1], z_bcu),
        (q1_t[0], q1_t[1], z_bcu),
    ]

    solids = []
    for i in range(len(path) - 1):
        seg = make_cylinder(path[i], path[i + 1], WIRE_R)
        if seg:
            solids.append(seg)
    for pt in path[1:-1]:
        solids.append(make_sphere(pt, WIRE_R))

    result = solids[0]
    for s in solids[1:]:
        result = result.fuse(s)
    return cq.Workplane("XY").newObject([result])


def make_footprint(pads, name, description):
    """Generate .kicad_mod with real THT pads and fab artwork."""
    origin = pads["ref1"]

    j1 = to_fp(*pads["j1"], origin)
    r1 = (0.0, 0.0)
    r2 = to_fp(*pads["ref2"], origin)
    q1 = to_fp(*pads["q1"], origin)

    j1_t = trim_point(j1, r1, END_TRIM)
    q1_t = trim_point(q1, r2, END_TRIM)

    uid = lambda: str(uuid.uuid4())

    fp = f"""(footprint "{name}"
	(version 20240108)
	(generator "generate_straps.py")
	(generator_version "3.0")
	(layer "F.Cu")
	(descr "{description}")
	(attr through_hole allow_missing_courtyard)
	(fp_text reference "REF**"
		(at {r2[0] / 2:.4f} {r2[1] / 2:.4f})
		(layer "F.SilkS")
		(uuid "{uid()}")
		(effects
			(font
				(size 1 1)
				(thickness 0.15)
			)
		)
	)
	(fp_text value "{name}"
		(at {r2[0] / 2:.4f} {r2[1] / 2 + 1.5:.4f})
		(layer "F.Fab")
		(hide yes)
		(uuid "{uid()}")
		(effects
			(font
				(size 1 1)
				(thickness 0.15)
			)
		)
	)
	(pad "1" thru_hole circle
		(at {r1[0]:.4f} {r1[1]:.4f})
		(size {PAD_SIZE} {PAD_SIZE})
		(drill {PAD_DRILL})
		(layers "*.Cu" "*.Mask")
		(remove_unused_layers no)
		(uuid "{uid()}")
	)
	(pad "2" thru_hole circle
		(at {r2[0]:.4f} {r2[1]:.4f})
		(size {PAD_SIZE} {PAD_SIZE})
		(drill {PAD_DRILL})
		(layers "*.Cu" "*.Mask")
		(remove_unused_layers no)
		(uuid "{uid()}")
	)
	(fp_line
		(start {j1_t[0]:.4f} {j1_t[1]:.4f})
		(end {r1[0]:.4f} {r1[1]:.4f})
		(stroke
			(width 0.5)
			(type dash)
		)
		(layer "B.Fab")
		(uuid "{uid()}")
	)
	(fp_line
		(start {r1[0]:.4f} {r1[1]:.4f})
		(end {r2[0]:.4f} {r2[1]:.4f})
		(stroke
			(width 0.5)
			(type solid)
		)
		(layer "F.Fab")
		(uuid "{uid()}")
	)
	(fp_line
		(start {r2[0]:.4f} {r2[1]:.4f})
		(end {q1_t[0]:.4f} {q1_t[1]:.4f})
		(stroke
			(width 0.5)
			(type dash)
		)
		(layer "B.Fab")
		(uuid "{uid()}")
	)
	(model "${{KIPRJMOD}}/../KiCad/3dmodels/{name}.step"
		(offset
			(xyz 0 0 0)
		)
		(scale
			(xyz 1 1 1)
		)
		(rotate
			(xyz 0 0 0)
		)
	)
)
"""
    return fp


if __name__ == "__main__":
    print(f"Wire diameter: {WIRE_D:.2f}mm")

    print("Generating LINE strap...")
    step = make_strap_step(LINE_PADS)
    cq.exporters.export(step, "../KiCad/3dmodels/CopperStrap_LINE.step")
    fp = make_footprint(LINE_PADS, "CopperStrap_LINE",
                        "1.5mm2 copper strap, LINE net, J1p1-pad1-pad2-Q1p2")
    with open("../KiCad/UserDef.pretty/CopperStrap_LINE.kicad_mod", "w") as f:
        f.write(fp)
    print("  -> STEP + footprint")

    print("Generating S/LINE strap...")
    step = make_strap_step(SLINE_PADS)
    cq.exporters.export(step, "../KiCad/3dmodels/CopperStrap_SLINE.step")
    fp = make_footprint(SLINE_PADS, "CopperStrap_SLINE",
                        "1.5mm2 copper strap, S/LINE net, J1p3-pad1-pad2-Q1p1")
    with open("../KiCad/UserDef.pretty/CopperStrap_SLINE.kicad_mod", "w") as f:
        f.write(fp)
    print("  -> STEP + footprint")

    print("""
Done! To use:
1. Remove REF1-REF4 test pad footprints from the PCB
2. Place CopperStrap_LINE at REF4 position (69.268, 40.003)
3. Place CopperStrap_SLINE at REF3 position (59.743, 40.003)
4. Assign pad 1 and pad 2 to the LINE / S_LINE net
""")
