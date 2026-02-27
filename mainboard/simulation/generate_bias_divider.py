#!/usr/bin/env python3
"""Generate bias_divider.kicad_sch — Realistic ADC Input Simulation.

This script produces a KiCad 9 schematic with two channels:
  Channel 1 (with bypass cap C11)  — realistic model of L1 voltage sensing
  Channel 2 (without bypass cap)   — comparison reference

New over previous version:
  - R_SRC Thevenin source impedance: Rw||R16 = 118||150 = 66 Ohm
  - C_TVS parasitic capacitance from TVS diodes (~100 pF)
  - ADC S/H switch model (voltage-controlled SWITCH, ron=1K)
  - C_SH sample-and-hold capacitor (14 pF)
  - V_CLK sampling clock (VPULSE ~9.6 kHz)
  - Reference designators match real mainboard (R101, R102, R17, C10, C11)
"""

import uuid as _uuid

# ─── Helpers ────────────────────────────────────────────────────────────

def uid():
    return str(_uuid.uuid4())


def c(v):
    """Round coordinate to 2 decimal places to avoid floating-point artifacts in output."""
    return round(v, 2)


ROOT_UUID = "4786b6dc-ecad-4b63-a8fd-84a0effc54c7"  # keep same as original

# ─── Library symbols (extracted from installed KiCad 9 libs) ────────────
from lib_symbols_extracted import (
    LIB_DEVICE_C, LIB_DEVICE_R,
    LIB_VDC, LIB_VSIN, LIB_VPULSE, LIB_SWITCH,
    LIB_GND, LIB_PWR_FLAG,
)

_UNUSED_LIB_SYMBOLS = '''\
		(symbol "Device:C"
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 0.254)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "C"
				(at 0.635 2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Value" "C"
				(at 0.635 -2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Footprint" ""
				(at 0.9652 -3.81 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" "~"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Unpolarized capacitor"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "C_0_1"
				(polyline
					(pts
						(xy -2.032 0.762) (xy 2.032 0.762)
					)
					(stroke
						(width 0.508)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy -2.032 -0.762) (xy 2.032 -0.762)
					)
					(stroke
						(width 0.508)
						(type default)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "C_1_1"
				(pin passive line
					(at 0 3.81 270)
					(length 2.794)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 0 -3.81 90)
					(length 2.794)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)'''

LIB_DEVICE_R = '''\
		(symbol "Device:R"
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 0)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "R"
				(at 2.032 0 90)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Value" "R"
				(at 0 0 90)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at -1.778 0 90)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" "~"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Resistor"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "R_0_1"
				(rectangle
					(start -1.016 -2.54)
					(end 1.016 2.54)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "R_1_1"
				(pin passive line
					(at 0 3.81 270)
					(length 1.27)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 0 -3.81 90)
					(length 1.27)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)'''

LIB_VDC = '''\
		(symbol "Simulation_SPICE:VDC"
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 0.0254)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "V"
				(at 2.54 2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Value" "1"
				(at 2.54 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" "~"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Voltage source, DC"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Sim.Pins" "1=+ 2=-"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Sim.Type" "DC"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Sim.Device" "V"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
					(hide yes)
				)
			)
			(symbol "VDC_0_0"
				(polyline
					(pts
						(xy -1.27 0.254) (xy 1.27 0.254)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy -0.762 -0.254) (xy -1.27 -0.254)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 0.254 -0.254) (xy -0.254 -0.254)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 1.27 -0.254) (xy 0.762 -0.254)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(text "+"
					(at 0 1.905 0)
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(symbol "VDC_0_1"
				(circle
					(center 0 0)
					(radius 2.54)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type background)
					)
				)
			)
			(symbol "VDC_1_1"
				(pin passive line
					(at 0 5.08 270)
					(length 2.54)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 0 -5.08 90)
					(length 2.54)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)'''

LIB_VSIN = '''\
		(symbol "Simulation_SPICE:VSIN"
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 0.0254)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "V"
				(at 2.54 2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Value" "VSIN"
				(at 2.54 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" "~"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Voltage source, sinusoidal"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Sim.Pins" "1=+ 2=-"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Sim.Params" "dc=0 ampl=1 f=1k ac=1"
				(at 2.54 -2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Sim.Type" "SIN"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Sim.Device" "V"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
					(hide yes)
				)
			)
			(symbol "VSIN_0_0"
				(arc
					(start -1.27 0)
					(mid -0.635 0.6323)
					(end 0 0)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(arc
					(start 1.27 0)
					(mid 0.635 -0.6323)
					(end 0 0)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(text "+"
					(at 0 1.905 0)
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(symbol "VSIN_0_1"
				(circle
					(center 0 0)
					(radius 2.54)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type background)
					)
				)
			)
			(symbol "VSIN_1_1"
				(pin passive line
					(at 0 5.08 270)
					(length 2.54)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 0 -5.08 90)
					(length 2.54)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)'''

LIB_VPULSE = '''\
		(symbol "Simulation_SPICE:VPULSE"
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 0.0254)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "V"
				(at 2.54 2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Value" "VPULSE"
				(at 2.54 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec_Independent_Sources_for"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Voltage source, pulse"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Sim.Pins" "1=+ 2=-"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Sim.Type" "PULSE"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Sim.Device" "V"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
					(hide yes)
				)
			)
			(property "Sim.Params" "y1=0 y2=1 td=2n tr=2n tf=2n tw=50n per=100n"
				(at 2.54 -2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "ki_keywords" "simulation"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "VPULSE_0_0"
				(polyline
					(pts
						(xy -2.032 -0.762) (xy -1.397 -0.762) (xy -1.143 0.762) (xy -0.127 0.762) (xy 0.127 -0.762) (xy 1.143 -0.762)
						(xy 1.397 0.762) (xy 2.032 0.762)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(text "+"
					(at 0 1.905 0)
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(symbol "VPULSE_0_1"
				(circle
					(center 0 0)
					(radius 2.54)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type background)
					)
				)
			)
			(symbol "VPULSE_1_1"
				(pin passive line
					(at 0 5.08 270)
					(length 2.54)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 0 -5.08 90)
					(length 2.54)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)'''

LIB_SWITCH = '''\
		(symbol "Simulation_SPICE:SWITCH"
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 1.016)
				(hide yes)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "S"
				(at 2.54 2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Value" "SWITCH"
				(at 2.54 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#subsec_Switches"
				(at 0 16.51 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Voltage controlled switch symbol for simulation only"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Sim.Device" "SW"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Sim.Type" "V"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Sim.Params" "thr=0 ron=1"
				(at 2.54 -2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Sim.Pins" "1=no+ 2=no- 3=ctrl+ 4=ctrl-"
				(at 0 13.97 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "ki_keywords" "simulation"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "SWITCH_0_1"
				(circle
					(center 0 2.032)
					(radius 0.508)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(circle
					(center 0 -2.032)
					(radius 0.508)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 0.254 1.524) (xy 1.778 -1.524)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "SWITCH_1_1"
				(circle
					(center -5.08 0)
					(radius 2.54)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type background)
					)
				)
				(polyline
					(pts
						(xy -4.826 3.81) (xy -4.318 3.81)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy -4.826 -3.81) (xy -4.318 -3.81)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy -4.572 4.064) (xy -4.572 3.556)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy -2.54 0) (xy 0.889 0)
					)
					(stroke
						(width 0)
						(type dash)
					)
					(fill
						(type none)
					)
				)
				(text "V"
					(at -5.08 0 0)
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(pin input line
					(at -5.08 5.08 270)
					(length 2.54)
					(name "C+"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "3"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin input line
					(at -5.08 -5.08 90)
					(length 2.54)
					(name "C-"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "4"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 0 5.08 270)
					(length 2.54)
					(name "N+"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 0 -5.08 90)
					(length 2.54)
					(name "N-"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)'''

LIB_GND = '''\
		(symbol "power:GND"
			(power)
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 0)
				(hide yes)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "#PWR"
				(at 0 -6.35 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Value" "GND"
				(at 0 -3.81 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Power symbol creates a global label with name \\"GND\\" , ground"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "GND_0_1"
				(polyline
					(pts
						(xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "GND_1_1"
				(pin power_in line
					(at 0 0 270)
					(length 0)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)'''  # noqa: unused — old inline defs kept for reference only


# ─── Emitters ──────────────────────────────────────────────────────────

def wire(x1, y1, x2, y2):
    return f'''\t(wire
\t\t(pts
\t\t\t(xy {c(x1)} {c(y1)}) (xy {c(x2)} {c(y2)})
\t\t)
\t\t(stroke
\t\t\t(width 0)
\t\t\t(type default)
\t\t)
\t\t(uuid "{uid()}")
\t)'''


def junction(x, y):
    return f'''\t(junction
\t\t(at {c(x)} {c(y)})
\t\t(diameter 0)
\t\t(color 0 0 0 0)
\t\t(uuid "{uid()}")
\t)'''


def label(name, x, y, angle=0):
    if angle == 0:
        just = "left bottom"
    elif angle == 90:
        just = "left bottom"
    else:
        just = "left bottom"
    return f'''\t(label "{name}"
\t\t(at {x} {y} {angle})
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify {just})
\t\t)
\t\t(uuid "{uid()}")
\t)'''


def text_annotation(txt, x, y, size=1.27, justify="left"):
    return f'''\t(text "{txt}"
\t\t(exclude_from_sim no)
\t\t(at {x} {y} 0)
\t\t(effects
\t\t\t(font
\t\t\t\t(size {size} {size})
\t\t\t)
\t\t\t(justify {justify})
\t\t)
\t\t(uuid "{uid()}")
\t)'''


def gnd_symbol(x, y, pwr_ref):
    """GND power symbol at position (x,y). Pin connects at (x,y)."""
    x, y = c(x), c(y)
    return f'''\t(symbol
\t\t(lib_id "power:GND")
\t\t(at {x} {y} 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{pwr_ref}"
\t\t\t(at {x} {y + 6.35} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Value" "GND"
\t\t\t(at {x} {y + 3.81} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Datasheet" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Description" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(pin "1"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(instances
\t\t\t(project "bias_divider"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{pwr_ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


def resistor(x, y, ref, value, rotation=0):
    """Resistor at (x,y). Default vertical: pin1 bottom (y+3.81), pin2 top (y-3.81).
    Rotation 90: horizontal, pin1 right (x+3.81), pin2 left (x-3.81). Passive, so polarity is irrelevant."""
    x, y = c(x), c(y)
    return f'''\t(symbol
\t\t(lib_id "Device:R")
\t\t(at {x} {y} {rotation})
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(fields_autoplaced yes)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {x + 2.54} {y} {rotation})
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Value" "{value}"
\t\t\t(at {x} {y} {rotation})
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Description" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(pin "1"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(pin "2"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(instances
\t\t\t(project "bias_divider"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


def capacitor(x, y, ref, value, rotation=0):
    """Capacitor at (x,y). Default vertical: pin1 bottom (y+3.81), pin2 top (y-3.81). Unpolarized."""
    x, y = c(x), c(y)
    return f'''\t(symbol
\t\t(lib_id "Device:C")
\t\t(at {x} {y} {rotation})
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(fields_autoplaced yes)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {x + 2.54} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Value" "{value}"
\t\t\t(at {x + 2.54} {y + 2.54} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Description" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(pin "1"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(pin "2"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(instances
\t\t\t(project "bias_divider"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


def vdc(x, y, ref, value, sim_value, rotation=180):
    """VDC source at (x,y). With rotation=180 (default): Pin1(+) at top (y-5.08), Pin2(-) at bottom (y+5.08)."""
    x, y = c(x), c(y)
    return f'''\t(symbol
\t\t(lib_id "Simulation_SPICE:VDC")
\t\t(at {x} {y} {rotation})
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {x + 2.54} {y + 2.54} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Value" "{value}"
\t\t\t(at {x + 2.54} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Description" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Sim.Pins" "1=+ 2=-"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Sim.Type" "DC"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Sim.Device" "V"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Sim.Params" "dc={sim_value}"
\t\t\t(at {x + 2.54} {y - 2.54} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(pin "1"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(pin "2"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(instances
\t\t\t(project "bias_divider"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


def vsin(x, y, ref, value, sim_params, rotation=180):
    """VSIN source at (x,y). With rotation=180 (default): Pin1(+) at top (y-5.08), Pin2(-) at bottom (y+5.08)."""
    x, y = c(x), c(y)
    return f'''\t(symbol
\t\t(lib_id "Simulation_SPICE:VSIN")
\t\t(at {x} {y} {rotation})
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {x + 2.54} {y + 2.54} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Value" "{value}"
\t\t\t(at {x + 2.54} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Description" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Sim.Pins" "1=+ 2=-"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Sim.Params" "{sim_params}"
\t\t\t(at {x + 2.54} {y - 2.54} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Sim.Type" "SIN"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Sim.Device" "V"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(pin "1"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(pin "2"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(instances
\t\t\t(project "bias_divider"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


def vpulse(x, y, ref, value, sim_params, rotation=180):
    """VPULSE source at (x,y). With rotation=180 (default): Pin1(+) at top (y-5.08), Pin2(-) at bottom (y+5.08)."""
    x, y = c(x), c(y)
    return f'''\t(symbol
\t\t(lib_id "Simulation_SPICE:VPULSE")
\t\t(at {x} {y} {rotation})
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {x + 2.54} {y + 2.54} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Value" "{value}"
\t\t\t(at {x + 2.54} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Description" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Sim.Pins" "1=+ 2=-"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Sim.Type" "PULSE"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Sim.Device" "V"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Sim.Params" "{sim_params}"
\t\t\t(at {x + 2.54} {y - 2.54} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(pin "1"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(pin "2"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(instances
\t\t\t(project "bias_divider"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


def switch(x, y, ref, sim_params, rotation=0):
    """Voltage-controlled switch at (x,y).
    Default orientation (0deg): N+/N- vertical, ctrl circle left.
    With rotation 90deg (used here for horizontal signal flow):
      Pin 1 (N+) at (x+5.08, y)   — right  (signal out)
      Pin 2 (N-) at (x-5.08, y)   — left   (signal in)
      Pin 3 (C+) at (x+5.08, y+5.08) — below-right (clock+)
      Pin 4 (C-) at (x-5.08, y+5.08) — below-left  (clock-)
    """
    x, y = c(x), c(y)
    return f'''\t(symbol
\t\t(lib_id "Simulation_SPICE:SWITCH")
\t\t(at {x} {y} {rotation})
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {x} {y - 7.62} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Value" "SWITCH"
\t\t\t(at {x} {y - 10.16} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Description" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Sim.Device" "SW"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Sim.Type" "V"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Sim.Params" "{sim_params}"
\t\t\t(at {x + 2.54} {y + 2.54} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Sim.Pins" "1=no+ 2=no- 3=ctrl+ 4=ctrl-"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(pin "1"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(pin "2"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(pin "3"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(pin "4"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(instances
\t\t\t(project "bias_divider"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


def pwr_flag(x, y, flg_ref):
    """PWR_FLAG at (x,y). Tells ERC that the net is driven (power output)."""
    x, y = c(x), c(y)
    return f'''\t(symbol
\t\t(lib_id "power:PWR_FLAG")
\t\t(at {x} {y} 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{flg_ref}"
\t\t\t(at {x} {y - 1.905} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Value" "PWR_FLAG"
\t\t\t(at {x} {y - 3.81} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Description" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(pin "1"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(instances
\t\t\t(project "bias_divider"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{flg_ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


# ─── Build the schematic ──────────────────────────────────────────────

def build():
    parts = []
    p = parts.append

    # ── Channel 1 coordinates (with bypass cap C11) ──
    # Main horizontal signal path at Y = 55.88
    Y1 = 55.88

    # V1 (1.1V VREF) — leftmost, vertical
    # Center at (22.86, 60.96), pin1(+) at (22.86, 55.88), pin2(-) at (22.86, 66.04)
    V1_x, V1_y = 22.86, 60.96
    p(vdc(V1_x, V1_y, "V1", "VDC", "1.1"))
    p(gnd_symbol(V1_x, V1_y + 5.08, "#PWR01"))  # GND at pin2
    p(pwr_flag(V1_x, V1_y + 5.08, "#FLG01"))   # PWR_FLAG tells ERC that GND net is driven

    # Wire from V1 pin1(+) to R101 pin1
    # V1 pin1 at (22.86, 55.88)
    p(wire(V1_x, V1_y - 5.08, 33.02, Y1))  # horizontal to R101

    # R101 (10K upper divider, horizontal)
    # Center at (36.83, 55.88), rot 90. Pin1 at (33.02, 55.88), Pin2 at (40.64, 55.88)
    R101_x, R101_y = 36.83, Y1
    p(resistor(R101_x, R101_y, "R101", "10K", 90))

    # Wire from R101 pin2 to BIAS node
    BIAS_x = 50.8
    p(wire(40.64, Y1, BIAS_x, Y1))

    # Label VREF on the V1-R101 wire
    p(label("VREF", 27.94, Y1))

    # BIAS node junction
    p(junction(BIAS_x, Y1))
    p(label("BIAS", BIAS_x + 2.54, Y1))

    # Wire down from BIAS to branch point
    BRANCH_y = Y1 + 7.62  # = 63.5
    p(wire(BIAS_x, Y1, BIAS_x, BRANCH_y))
    p(junction(BIAS_x, BRANCH_y))

    # R102 (10K lower divider, vertical) — below BIAS
    # Center at (BIAS_x, 71.12). Pin1 at (BIAS_x, 67.31), Pin2 at (BIAS_x, 74.93)
    R102_x, R102_y = BIAS_x, 71.12
    p(resistor(R102_x, R102_y, "R102", "10K", 0))
    p(wire(BIAS_x, BRANCH_y, BIAS_x, R102_y - 3.81))  # branch to R102 pin1
    p(gnd_symbol(R102_x, R102_y + 3.81, "#PWR02"))  # GND below R102

    # C11 (100nF bypass, vertical) — parallel to R102, offset right
    C11_x = BIAS_x + 10.16  # = 60.96
    C11_y = 71.12
    p(capacitor(C11_x, C11_y, "C11", "100n", 0))
    p(wire(BIAS_x, BRANCH_y, C11_x, BRANCH_y))  # horizontal to C11 branch
    p(wire(C11_x, BRANCH_y, C11_x, C11_y - 3.81))  # down to C11 pin1
    p(gnd_symbol(C11_x, C11_y + 3.81, "#PWR03"))  # GND below C11

    # AC signal chain: from BIAS down through C10 → R_SRC → V2
    # R_SRC = Thevenin source impedance: Rw || R16 = 118 || 150 = 66 Ohm
    # (Rw = ZMPT101K secondary winding resistance = 118 Ohm measured)
    # (R16 = 150 Ohm burden across secondary)
    # C10 (10µF inline coupling, vertical) — below branch, to left of R102
    C10_x = BIAS_x - 10.16  # = 40.64
    C10_y = 71.12
    p(capacitor(C10_x, C10_y, "C10", "10u", 0))
    p(wire(BIAS_x, BRANCH_y, C10_x, BRANCH_y))  # horizontal left to C10 branch
    p(wire(C10_x, BRANCH_y, C10_x, C10_y - 3.81))  # down to C10 pin1

    # R_SRC (Thevenin 66 Ohm, vertical) — below C10
    RSRC_x, RSRC_y = C10_x, 83.82
    p(resistor(RSRC_x, RSRC_y, "R_SRC", "66", 0))
    p(wire(C10_x, C10_y + 3.81, RSRC_x, RSRC_y - 3.81))  # C10 pin2 to R_SRC pin1

    # V2 (VSIN 50Hz) — below R_SRC
    V2_x, V2_y = RSRC_x, 96.52
    p(vsin(V2_x, V2_y, "V2", "VSIN", "dc=0 ampl=0.407 f=50 ac=0.407"))
    p(wire(RSRC_x, RSRC_y + 3.81, V2_x, V2_y - 5.08))  # R_SRC pin2 to V2 pin1(+)
    p(gnd_symbol(V2_x, V2_y + 5.08, "#PWR04"))  # GND below V2

    # Label SIG on the AC source output (between C10 and R_SRC)
    p(label("SIG", C10_x, C10_y + 3.81 + 1.27, 0))

    # ── Right side: R17 → ADC_PIN → C_TVS, then SW1 → C_SH ──

    # R17 (1K protection, horizontal)
    R17_x, R17_y = 63.5, Y1
    p(resistor(R17_x, R17_y, "R17", "1K", 90))
    # Wire from BIAS to R17 pin1
    p(wire(BIAS_x, Y1, R17_x - 3.81, Y1))

    # ADC_PIN node
    ADC_x = 76.2
    p(wire(R17_x + 3.81, Y1, ADC_x, Y1))  # R17 pin2 to ADC_PIN
    p(junction(ADC_x, Y1))
    p(label("ADC_PIN", ADC_x + 1.27, Y1))

    # C_TVS (100pF TVS parasitic, vertical) — below ADC_PIN
    CTVS_x, CTVS_y = ADC_x, 68.58
    p(capacitor(CTVS_x, CTVS_y, "C_TVS1", "100p", 0))
    p(wire(ADC_x, Y1, CTVS_x, CTVS_y - 3.81))  # ADC_PIN down to C_TVS pin1
    p(gnd_symbol(CTVS_x, CTVS_y + 3.81, "#PWR05"))  # GND below C_TVS

    # SW1 (ADC S/H switch, rotated 90° for horizontal signal flow)
    # With 90° rotation:
    #   Pin 1 (N+) at (x+5.08, y)   — right
    #   Pin 2 (N-) at (x-5.08, y)   — left
    #   Pin 3 (C+) at (x+5.08, y+5.08) — below-right
    #   Pin 4 (C-) at (x-5.08, y+5.08) — below-left
    SW1_x, SW1_y = 91.44, Y1
    p(switch(SW1_x, SW1_y, "S1", "thr=0.5 roff=1e12 ron=1K", 90))

    # Wire ADC_PIN to SW1 pin2(N-) (left side)
    p(wire(ADC_x, Y1, SW1_x - 5.08, Y1))

    # C_SH (14pF S/H cap, vertical) — to the right of SW1
    CSH_x = SW1_x + 5.08  # = 96.52 — at SW1 pin1(N+)
    CSH_y = 68.58
    p(capacitor(CSH_x, CSH_y, "C_SH1", "14p", 0))
    p(wire(CSH_x, Y1, CSH_x, CSH_y - 3.81))  # SW1 N+ down to C_SH pin1
    p(gnd_symbol(CSH_x, CSH_y + 3.81, "#PWR06"))  # GND below C_SH

    # Label on SW1 output — stub wire so label is on a wire endpoint
    SH1_label_x = CSH_x + 5.08
    p(wire(CSH_x, Y1, SH1_label_x, Y1))
    p(label("SH1", SH1_label_x, Y1))

    # V_CLK (VPULSE sampling clock) — below SW1
    # SW1 pin3(C+) at (SW1_x+5.08, SW1_y+5.08) = (96.52, 60.96)
    # SW1 pin4(C-) at (SW1_x-5.08, SW1_y+5.08) = (86.36, 60.96)
    # V_CLK connects: pin1(+) to C+, pin2(-) to C-
    VCLK_x = SW1_x
    VCLK_y = SW1_y + 5.08 + 12.7  # = 73.66
    # V_CLK centered between the two control pins
    p(vpulse(VCLK_x, VCLK_y, "V3", "VPULSE",
             "y1=0 y2=1 td=0 tr=1n tf=1n tw=12u per=104.2u"))

    # Wire V_CLK pin1(+) at (VCLK_x, VCLK_y-5.08) up to SW1 pin3(C+)
    # SW1 C+ is at (SW1_x+5.08, SW1_y+5.08) = (96.52, 60.96)
    p(wire(VCLK_x, VCLK_y - 5.08, VCLK_x, SW1_y + 5.08))
    # Now horizontal wire to SW1 C+ pin
    p(wire(VCLK_x, SW1_y + 5.08, SW1_x + 5.08, SW1_y + 5.08))

    # GND for V_CLK pin2(-) at (VCLK_x, VCLK_y+5.08)
    p(gnd_symbol(VCLK_x, VCLK_y + 5.08, "#PWR07"))

    # Wire from V_CLK GND area to SW1 pin4(C-)
    # SW1 C- is at (SW1_x-5.08, SW1_y+5.08) = (86.36, 60.96)
    # Connect GND to C- directly
    p(wire(SW1_x - 5.08, SW1_y + 5.08, SW1_x - 5.08, SW1_y + 5.08 + 2.54))
    p(gnd_symbol(SW1_x - 5.08, SW1_y + 5.08 + 2.54, "#PWR08"))

    # ── Channel 2 (without bypass cap — comparison) ──
    # Offset Y by 80mm
    DY = 78.74  # 31 × 2.54mm — must be grid-aligned
    Y2 = Y1 + DY  # = 135.88

    # V4 (1.1V VREF) for channel 2
    p(vdc(V1_x, V1_y + DY, "V4", "VDC", "1.1"))
    p(gnd_symbol(V1_x, V1_y + DY + 5.08, "#PWR09"))

    # Wire from V4 pin1(+) to R201 pin1
    p(wire(V1_x, V1_y + DY - 5.08, 33.02, Y2))

    # R201 (10K upper divider, horizontal)
    p(resistor(R101_x, Y2, "R201", "10K", 90))
    p(wire(40.64, Y2, BIAS_x, Y2))

    p(label("VREF_NF", 27.94, Y2))

    # BIAS_NF node
    p(junction(BIAS_x, Y2))
    p(label("BIAS_NF", BIAS_x + 2.54, Y2))

    # Wire down from BIAS_NF
    BRANCH2_y = Y2 + 7.62
    p(wire(BIAS_x, Y2, BIAS_x, BRANCH2_y))
    p(junction(BIAS_x, BRANCH2_y))

    # R202 (10K lower divider)
    R202_y = 71.12 + DY
    p(resistor(BIAS_x, R202_y, "R202", "10K", 0))
    p(wire(BIAS_x, BRANCH2_y, BIAS_x, R202_y - 3.81))
    p(gnd_symbol(BIAS_x, R202_y + 3.81, "#PWR010"))

    # NO C11 in channel 2 (that's the point of comparison)

    # AC signal chain for channel 2
    C20_x = C10_x
    C20_y = C10_y + DY
    p(capacitor(C20_x, C20_y, "C20", "10u", 0))
    p(wire(BIAS_x, BRANCH2_y, C20_x, BRANCH2_y))
    p(wire(C20_x, BRANCH2_y, C20_x, C20_y - 3.81))

    R26_y = RSRC_y + DY
    p(resistor(C20_x, R26_y, "R26", "66", 0))
    p(wire(C20_x, C20_y + 3.81, C20_x, R26_y - 3.81))

    V5_y = V2_y + DY
    p(vsin(C20_x, V5_y, "V5", "VSIN", "dc=0 ampl=0.407 f=50 ac=0.407"))
    p(wire(C20_x, R26_y + 3.81, C20_x, V5_y - 5.08))
    p(gnd_symbol(C20_x, V5_y + 5.08, "#PWR011"))

    p(label("SIG_NF", C20_x, C20_y + 3.81 + 1.27, 0))

    # R27 (1K protection)
    R27_x = R17_x
    p(resistor(R27_x, Y2, "R27", "1K", 90))
    p(wire(BIAS_x, Y2, R27_x - 3.81, Y2))

    # ADC_NF node
    p(wire(R27_x + 3.81, Y2, ADC_x, Y2))
    p(junction(ADC_x, Y2))
    p(label("ADC_NF", ADC_x + 1.27, Y2))

    # C_TVS2 (100pF)
    CTVS2_y = CTVS_y + DY
    p(capacitor(ADC_x, CTVS2_y, "C_TVS2", "100p", 0))
    p(wire(ADC_x, Y2, ADC_x, CTVS2_y - 3.81))
    p(gnd_symbol(ADC_x, CTVS2_y + 3.81, "#PWR012"))

    # SW2 (ADC switch)
    SW2_x, SW2_y = SW1_x, Y2
    p(switch(SW2_x, SW2_y, "S2", "thr=0.5 roff=1e12 ron=1K", 90))
    p(wire(ADC_x, Y2, SW2_x - 5.08, Y2))

    # C_SH2 (14pF)
    CSH2_x = SW2_x + 5.08
    CSH2_y = CTVS2_y
    p(capacitor(CSH2_x, CSH2_y, "C_SH2", "14p", 0))
    p(wire(CSH2_x, Y2, CSH2_x, CSH2_y - 3.81))
    p(gnd_symbol(CSH2_x, CSH2_y + 3.81, "#PWR013"))

    SH2_label_x = CSH2_x + 5.08
    p(wire(CSH2_x, Y2, SH2_label_x, Y2))
    p(label("SH2", SH2_label_x, Y2))

    # V_CLK2 for channel 2 (same parameters)
    VCLK2_x = SW2_x
    VCLK2_y = SW2_y + 5.08 + 12.7
    p(vpulse(VCLK2_x, VCLK2_y, "V6", "VPULSE",
             "y1=0 y2=1 td=0 tr=1n tf=1n tw=12u per=104.2u"))
    p(wire(VCLK2_x, VCLK2_y - 5.08, VCLK2_x, SW2_y + 5.08))
    p(wire(VCLK2_x, SW2_y + 5.08, SW2_x + 5.08, SW2_y + 5.08))
    p(gnd_symbol(VCLK2_x, VCLK2_y + 5.08, "#PWR014"))

    # GND for SW2 C-
    p(wire(SW2_x - 5.08, SW2_y + 5.08, SW2_x - 5.08, SW2_y + 5.08 + 2.54))
    p(gnd_symbol(SW2_x - 5.08, SW2_y + 5.08 + 2.54, "#PWR015"))

    # ── Text annotations ──
    TX = 120.0
    TY_start = 40.0

    p(text_annotation(
        "VREF/2 Bias Divider — Realistic ADC Input Simulation",
        29.21, 30.48, size=2.5))
    p(text_annotation(
        "PVRouter Mainboard — ZMPT101K voltage sensing channel (L1)",
        29.21, 35.56, size=1.5))

    p(text_annotation("Component Legend (sim ref → real board ref):", TX, TY_start, size=1.5))
    legend = [
        "V1: LMV321A buffered 1.1V AREF (U2 output)",
        "R101/R102: VREF/2 bias divider (10K/10K) — DC midpoint ~0.55V",
        "C11: Bypass cap across R102 (100nF) — Ch1 only, Ch2 omits for comparison",
        "C10: Inline AC coupling cap (10uF) — blocks DC from sensor",
        "R_SRC: Thevenin Zth = Rw || R16 = 118 || 150 = 66 Ohm",
        "  (Rw = ZMPT101K secondary winding resistance, measured)",
        "V2: ZMPT101K output (0.407V pk at 230V mains, 50Hz)",
        "R17: Series ADC protection resistor (1K)",
        "C_TVS: TVS diode parasitic capacitance (D11+D12 DF2B7AE, ~100pF total)",
        "S1/S2: ATmega328P ADC S/H switch model (ron=1K, thr=0.5V)",
        "C_SH: ADC internal S/H capacitor (14pF)",
        "V3/V6: Sampling clock (~9.6kHz, 12us on / 92us off)",
    ]
    for i, line in enumerate(legend):
        p(text_annotation(f"  {line}", TX, TY_start + 3.81 + i * 3.0, size=1.27))

    sim_y = TY_start + 3.81 + len(legend) * 3.0 + 5.08
    p(text_annotation("Simulation Commands (Inspect > Simulator):", TX, sim_y, size=1.5))
    p(text_annotation("  Transient: .tran 10u 100m", TX, sim_y + 3.81, size=1.27))
    p(text_annotation("    Probe: BIAS, ADC_PIN, SH1 (Ch1) vs BIAS_NF, ADC_NF, SH2 (Ch2)", TX, sim_y + 6.35, size=1.27))
    p(text_annotation("  AC analysis: .ac dec 200 0.1 100k", TX, sim_y + 8.89, size=1.27))
    p(text_annotation("    Probe: BIAS and ADC_PIN — compare Ch1 vs Ch2", TX, sim_y + 11.43, size=1.27))
    p(text_annotation("  Expected: BIAS settles ~0.55V, 50Hz sine visible, S/H stepping on SH1/SH2", TX, sim_y + 13.97, size=1.27))

    # Channel labels
    p(text_annotation("Channel 1 — With bypass cap C11 (100nF)", 22.86, Y1 - 10.16, size=1.5))
    p(text_annotation("Channel 2 — Without bypass cap (comparison)", 22.86, Y2 - 10.16, size=1.5))

    return parts


# ─── Assemble final schematic ─────────────────────────────────────────

def main():
    parts = build()

    header = f'''(kicad_sch
\t(version 20250114)
\t(generator "eeschema")
\t(generator_version "9.0")
\t(uuid "{ROOT_UUID}")
\t(paper "A3")
\t(title_block
\t\t(title "VREF/2 Bias Divider — Realistic ADC Input Simulation")
\t\t(date "2026-02-24")
\t\t(rev "3.0")
\t\t(company "PVRouter — ADC input simulation")
\t\t(comment 1 "PVRouter Mainboard — ZMPT101K voltage sensing channel (L1)")
\t\t(comment 2 "Includes: Zth=66 Ohm (Rw||R16), TVS parasitic C, ADC S/H switch model")
\t)
\t(lib_symbols
{LIB_DEVICE_C}
{LIB_DEVICE_R}
{LIB_VDC}
{LIB_VSIN}
{LIB_VPULSE}
{LIB_SWITCH}
{LIB_GND}
{LIB_PWR_FLAG}
\t)'''

    footer = ')'

    with open("bias_divider.kicad_sch", "w") as f:
        f.write(header + "\n")
        for part in parts:
            f.write(part + "\n")
        f.write(footer + "\n")

    print("Generated bias_divider.kicad_sch")


if __name__ == "__main__":
    main()
