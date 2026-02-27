#!/usr/bin/env python3
"""Generate combined_bias_divider.kicad_sch — Voltage vs CT Channel Comparison.

This script produces a KiCad 9 schematic with two channels for direct comparison:
  Channel 1: Voltage sensing (ZMPT101K) — Zth=66 Ohm (Rw=118||R16=150), C_TVS 100pF, C11 bypass
  Channel 2: CT current sensing — no burden, C_TVS_CT 50pF at source, C_TVS_ADC 50pF, C13 bypass

Both channels include their respective bypass caps.

ZMPT101K source impedance model:
  Rw = 118 Ohm (secondary winding resistance, measured)
  R16 = 150 Ohm (burden resistor, across secondary)
  Thevenin impedance: Zth = Rw || R16 = 118*150/(118+150) = 66 Ohm
"""

import uuid as _uuid

# ─── Helpers ────────────────────────────────────────────────────────────

def uid():
    return str(_uuid.uuid4())


def c(v):
    """Round coordinate to 2 decimal places to avoid floating-point artifacts in output."""
    return round(v, 2)


PROJECT = "combined_bias_divider"
ROOT_UUID = "7b04e9cf-2d56-4f8b-b3e0-84d1f6a23c57"

# ─── Library symbols (extracted from installed KiCad 9 libs) ────────────
from lib_symbols_extracted import (
    LIB_DEVICE_C, LIB_DEVICE_R,
    LIB_VDC, LIB_VSIN, LIB_VPULSE, LIB_SWITCH,
    LIB_GND, LIB_PWR_FLAG,
)


# ─── S-expression emitters ──────────────────────────────────────────────

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
\t\t\t(project "{PROJECT}"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{pwr_ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


def resistor(x, y, ref, value, rotation=0):
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
\t\t\t(project "{PROJECT}"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


def capacitor(x, y, ref, value, rotation=0):
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
\t\t\t(project "{PROJECT}"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


def vdc(x, y, ref, value, sim_value, rotation=180):
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
\t\t\t(project "{PROJECT}"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


def vsin(x, y, ref, value, sim_params, rotation=180):
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
\t\t\t(project "{PROJECT}"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


def vpulse(x, y, ref, value, sim_params, rotation=180):
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
\t\t\t(project "{PROJECT}"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


def switch(x, y, ref, sim_params, rotation=0):
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
\t\t\t(project "{PROJECT}"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


def pwr_flag(x, y, flg_ref):
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
\t\t\t(project "{PROJECT}"
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

    # ════════════════════════════════════════════════════════════════════
    # Channel 1 — VOLTAGE SENSING (ZMPT101K)
    #   R_SRC = Zth = Rw||R16 = 118||150 = 66 Ohm, C_TVS (100pF), C11 bypass
    # ════════════════════════════════════════════════════════════════════
    Y1 = 55.88

    # V1 (1.1V VREF)
    V1_x, V1_y = 22.86, 60.96
    p(vdc(V1_x, V1_y, "V1", "VDC", "1.1"))
    p(gnd_symbol(V1_x, V1_y + 5.08, "#PWR01"))
    p(pwr_flag(V1_x, V1_y + 5.08, "#FLG01"))

    # Wire from V1 pin1(+) to R101
    p(wire(V1_x, V1_y - 5.08, 33.02, Y1))

    # R101 (10K upper divider, horizontal)
    R101_x = 36.83
    p(resistor(R101_x, Y1, "R101", "10K", 90))

    BIAS_x = 50.8
    p(wire(40.64, Y1, BIAS_x, Y1))
    p(label("VREF_V", 27.94, Y1))

    # BIAS_V node
    p(junction(BIAS_x, Y1))
    p(label("BIAS_V", BIAS_x + 2.54, Y1))

    BRANCH_y = Y1 + 7.62
    p(wire(BIAS_x, Y1, BIAS_x, BRANCH_y))
    p(junction(BIAS_x, BRANCH_y))

    # R102 (10K lower divider)
    R102_y = 71.12
    p(resistor(BIAS_x, R102_y, "R102", "10K", 0))
    p(wire(BIAS_x, BRANCH_y, BIAS_x, R102_y - 3.81))
    p(gnd_symbol(BIAS_x, R102_y + 3.81, "#PWR02"))

    # C11 (100nF bypass) — parallel to R102
    C11_x = BIAS_x + 10.16
    p(capacitor(C11_x, R102_y, "C11", "100n", 0))
    p(wire(BIAS_x, BRANCH_y, C11_x, BRANCH_y))
    p(wire(C11_x, BRANCH_y, C11_x, R102_y - 3.81))
    p(gnd_symbol(C11_x, R102_y + 3.81, "#PWR03"))

    # AC signal chain: C10 → R_SRC (Thevenin 66 Ohm) → V2
    # R_SRC = Rw || R16 = 118 || 150 = 66 Ohm
    # (Rw = ZMPT101K secondary winding resistance = 118 Ohm measured)
    # (R16 = 150 Ohm burden across secondary)
    C10_x = BIAS_x - 10.16  # = 40.64
    C10_y = 71.12
    p(capacitor(C10_x, C10_y, "C10", "10u", 0))
    p(wire(BIAS_x, BRANCH_y, C10_x, BRANCH_y))
    p(wire(C10_x, BRANCH_y, C10_x, C10_y - 3.81))

    # R_SRC (Thevenin source impedance: Rw || R16 = 118 || 150 = 66 Ohm)
    RSRC_x, RSRC_y = C10_x, 83.82
    p(resistor(RSRC_x, RSRC_y, "R_SRC", "66", 0))
    p(wire(C10_x, C10_y + 3.81, RSRC_x, RSRC_y - 3.81))

    # V2 (VSIN 50Hz) — below R_SRC
    V2_x, V2_y = RSRC_x, 96.52
    p(vsin(V2_x, V2_y, "V2", "VSIN", "dc=0 ampl=0.407 f=50 ac=0.407"))
    p(wire(RSRC_x, RSRC_y + 3.81, V2_x, V2_y - 5.08))
    p(gnd_symbol(V2_x, V2_y + 5.08, "#PWR04"))

    p(label("SIG_V", C10_x, C10_y + 3.81 + 1.27, 0))

    # R17 (1K protection)
    R17_x = 63.5
    p(resistor(R17_x, Y1, "R17", "1K", 90))
    p(wire(BIAS_x, Y1, R17_x - 3.81, Y1))

    # ADC_V node
    ADC_x = 76.2
    p(wire(R17_x + 3.81, Y1, ADC_x, Y1))
    p(junction(ADC_x, Y1))
    p(label("ADC_V", ADC_x + 1.27, Y1))

    # C_TVS_V (100pF — D11+D12 combined)
    CTVS_V_y = 68.58
    p(capacitor(ADC_x, CTVS_V_y, "C_TVS_V", "100p", 0))
    p(wire(ADC_x, Y1, ADC_x, CTVS_V_y - 3.81))
    p(gnd_symbol(ADC_x, CTVS_V_y + 3.81, "#PWR05"))

    # SW1 (ADC S/H switch)
    SW1_x = 91.44
    p(switch(SW1_x, Y1, "S1", "thr=0.5 roff=1e12 ron=1K", 90))
    p(wire(ADC_x, Y1, SW1_x - 5.08, Y1))

    # C_SH1 (14pF)
    CSH_x = SW1_x + 5.08
    p(capacitor(CSH_x, CTVS_V_y, "C_SH1", "14p", 0))
    p(wire(CSH_x, Y1, CSH_x, CTVS_V_y - 3.81))
    p(gnd_symbol(CSH_x, CTVS_V_y + 3.81, "#PWR06"))

    SH1_label_x = CSH_x + 5.08
    p(wire(CSH_x, Y1, SH1_label_x, Y1))
    p(label("SH_V", SH1_label_x, Y1))

    # V_CLK1
    VCLK_x = SW1_x
    VCLK_y = Y1 + 5.08 + 12.7
    p(vpulse(VCLK_x, VCLK_y, "V3", "VPULSE",
             "y1=0 y2=1 td=0 tr=1n tf=1n tw=12u per=104.2u"))
    p(wire(VCLK_x, VCLK_y - 5.08, VCLK_x, Y1 + 5.08))
    p(wire(VCLK_x, Y1 + 5.08, SW1_x + 5.08, Y1 + 5.08))
    p(gnd_symbol(VCLK_x, VCLK_y + 5.08, "#PWR07"))

    p(wire(SW1_x - 5.08, Y1 + 5.08, SW1_x - 5.08, Y1 + 5.08 + 2.54))
    p(gnd_symbol(SW1_x - 5.08, Y1 + 5.08 + 2.54, "#PWR08"))

    # ════════════════════════════════════════════════════════════════════
    # Channel 2 — CT CURRENT SENSING
    #   No burden, C_TVS_CT (50pF D13 at source), C_TVS_ADC (50pF D12), C13 bypass
    # ════════════════════════════════════════════════════════════════════
    DY = 78.74
    Y2 = Y1 + DY

    # V4 (1.1V VREF)
    p(vdc(V1_x, V1_y + DY, "V4", "VDC", "1.1"))
    p(gnd_symbol(V1_x, V1_y + DY + 5.08, "#PWR09"))

    p(wire(V1_x, V1_y + DY - 5.08, 33.02, Y2))

    # R103 (10K upper divider)
    p(resistor(R101_x, Y2, "R103", "10K", 90))
    p(wire(40.64, Y2, BIAS_x, Y2))
    p(label("VREF_CT", 27.94, Y2))

    # BIAS_CT node
    p(junction(BIAS_x, Y2))
    p(label("BIAS_CT", BIAS_x + 2.54, Y2))

    BRANCH2_y = Y2 + 7.62
    p(wire(BIAS_x, Y2, BIAS_x, BRANCH2_y))
    p(junction(BIAS_x, BRANCH2_y))

    # R104 (10K lower divider)
    R104_y = R102_y + DY
    p(resistor(BIAS_x, R104_y, "R104", "10K", 0))
    p(wire(BIAS_x, BRANCH2_y, BIAS_x, R104_y - 3.81))
    p(gnd_symbol(BIAS_x, R104_y + 3.81, "#PWR010"))

    # C13 (100nF bypass) — parallel to R104
    p(capacitor(C11_x, R104_y, "C13", "100n", 0))
    p(wire(BIAS_x, BRANCH2_y, C11_x, BRANCH2_y))
    p(wire(C11_x, BRANCH2_y, C11_x, R104_y - 3.81))
    p(gnd_symbol(C11_x, R104_y + 3.81, "#PWR011"))

    # AC signal chain: C12 → V5 (no burden), with C_TVS_CT in parallel
    C12_x = C10_x
    C12_y = C10_y + DY
    p(capacitor(C12_x, C12_y, "C12", "10u", 0))
    p(wire(BIAS_x, BRANCH2_y, C12_x, BRANCH2_y))
    p(wire(C12_x, BRANCH2_y, C12_x, C12_y - 3.81))

    # SIG_CT junction — below C12 pin2
    SIG_CT_y = C12_y + 3.81
    p(junction(C12_x, SIG_CT_y))

    # V5 (VSIN 50Hz) — directly below C12 (no burden)
    V5_x, V5_y = C12_x, 83.82 + DY
    p(vsin(V5_x, V5_y, "V5", "VSIN", "dc=0 ampl=0.407 f=50 ac=0.407"))
    p(wire(C12_x, SIG_CT_y, V5_x, V5_y - 5.08))
    p(gnd_symbol(V5_x, V5_y + 5.08, "#PWR012"))

    # C_TVS_CT (50pF — D13 parasitic across CT pins) — parallel with V5
    CTVS_CT_x = C12_x - 10.16
    CTVS_CT_y = 83.82 + DY
    p(capacitor(CTVS_CT_x, CTVS_CT_y, "C_TVS_CT", "50p", 0))
    p(wire(C12_x, SIG_CT_y, CTVS_CT_x, SIG_CT_y))
    p(wire(CTVS_CT_x, SIG_CT_y, CTVS_CT_x, CTVS_CT_y - 3.81))
    p(gnd_symbol(CTVS_CT_x, CTVS_CT_y + 3.81, "#PWR013"))

    p(label("SIG_CT", C12_x + 1.27, SIG_CT_y, 0))

    # R19 (1K protection)
    R19_x = R17_x
    p(resistor(R19_x, Y2, "R19", "1K", 90))
    p(wire(BIAS_x, Y2, R19_x - 3.81, Y2))

    # ADC_CT node
    p(wire(R19_x + 3.81, Y2, ADC_x, Y2))
    p(junction(ADC_x, Y2))
    p(label("ADC_CT", ADC_x + 1.27, Y2))

    # C_TVS_ADC (50pF — D12 only)
    CTVS_ADC_y = CTVS_V_y + DY
    p(capacitor(ADC_x, CTVS_ADC_y, "C_TVS_ADC", "50p", 0))
    p(wire(ADC_x, Y2, ADC_x, CTVS_ADC_y - 3.81))
    p(gnd_symbol(ADC_x, CTVS_ADC_y + 3.81, "#PWR014"))

    # SW2 (ADC switch)
    SW2_x = SW1_x
    p(switch(SW2_x, Y2, "S2", "thr=0.5 roff=1e12 ron=1K", 90))
    p(wire(ADC_x, Y2, SW2_x - 5.08, Y2))

    # C_SH2 (14pF)
    CSH2_x = SW2_x + 5.08
    p(capacitor(CSH2_x, CTVS_ADC_y, "C_SH2", "14p", 0))
    p(wire(CSH2_x, Y2, CSH2_x, CTVS_ADC_y - 3.81))
    p(gnd_symbol(CSH2_x, CTVS_ADC_y + 3.81, "#PWR015"))

    SH2_label_x = CSH2_x + 5.08
    p(wire(CSH2_x, Y2, SH2_label_x, Y2))
    p(label("SH_CT", SH2_label_x, Y2))

    # V_CLK2
    VCLK2_x = SW2_x
    VCLK2_y = Y2 + 5.08 + 12.7
    p(vpulse(VCLK2_x, VCLK2_y, "V6", "VPULSE",
             "y1=0 y2=1 td=0 tr=1n tf=1n tw=12u per=104.2u"))
    p(wire(VCLK2_x, VCLK2_y - 5.08, VCLK2_x, Y2 + 5.08))
    p(wire(VCLK2_x, Y2 + 5.08, SW2_x + 5.08, Y2 + 5.08))
    p(gnd_symbol(VCLK2_x, VCLK2_y + 5.08, "#PWR016"))

    p(wire(SW2_x - 5.08, Y2 + 5.08, SW2_x - 5.08, Y2 + 5.08 + 2.54))
    p(gnd_symbol(SW2_x - 5.08, Y2 + 5.08 + 2.54, "#PWR017"))

    # ── Text annotations ──
    TX = 120.0
    TY_start = 40.0

    p(text_annotation(
        "Voltage vs CT Channel — ADC Input Comparison",
        29.21, 30.48, size=2.5))
    p(text_annotation(
        "PVRouter Mainboard — Direct comparison of voltage and CT sensing channels",
        29.21, 35.56, size=1.5))

    p(text_annotation("Component Legend:", TX, TY_start, size=1.5))
    legend = [
        "VOLTAGE CHANNEL (top):",
        "  R101/R102 (10K/10K), C11 (100nF bypass), C10 (10uF coupling)",
        "  R_SRC: Thevenin Zth = Rw || R16 = 118 || 150 = 66 Ohm",
        "    (Rw = ZMPT101K secondary winding resistance, measured)",
        "    (R16 = 150 Ohm burden across secondary)",
        "  C_TVS_V: D11+D12 TVS parasitic (100pF total)",
        "  R17: Series protection (1K)",
        "",
        "CT CHANNEL (bottom):",
        "  R103/R104 (10K/10K), C13 (100nF bypass), C12 (10uF coupling)",
        "  No burden — voltage-output CT has low source impedance",
        "  C_TVS_CT: D13 TVS parasitic across CT pins (50pF)",
        "  C_TVS_ADC: D12 TVS parasitic at ADC input (50pF)",
        "  R19: Series protection (1K)",
        "",
        "Both channels: V_AREF=1.1V, V_SIG=0.407Vpk 50Hz, ADC S/H ~9.6kHz",
    ]
    for i, line in enumerate(legend):
        p(text_annotation(f"  {line}", TX, TY_start + 3.81 + i * 3.0, size=1.27))

    sim_y = TY_start + 3.81 + len(legend) * 3.0 + 5.08
    p(text_annotation("Simulation Commands:", TX, sim_y, size=1.5))
    p(text_annotation("  AC analysis: .ac dec 200 0.1 100k", TX, sim_y + 3.81, size=1.27))
    p(text_annotation("    Probe: ADC_V vs ADC_CT — compare frequency response", TX, sim_y + 6.35, size=1.27))
    p(text_annotation("  Transient: .tran 10u 100m", TX, sim_y + 8.89, size=1.27))
    p(text_annotation("    Probe: BIAS_V vs BIAS_CT, ADC_V vs ADC_CT, SH_V vs SH_CT", TX, sim_y + 11.43, size=1.27))

    # Channel labels
    p(text_annotation("Channel 1 — Voltage sensing (ZMPT101K, Zth=66 Ohm, C_TVS=100pF)", 22.86, Y1 - 10.16, size=1.5))
    p(text_annotation("Channel 2 — CT current sensing (no burden, C_TVS_CT=50pF, C_TVS_ADC=50pF)", 22.86, Y2 - 10.16, size=1.5))

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
\t\t(title "Voltage vs CT Channel — ADC Input Comparison")
\t\t(date "2026-02-24")
\t\t(rev "1.0")
\t\t(company "PVRouter — ADC input simulation")
\t\t(comment 1 "Direct comparison: voltage sensing (ZMPT101K) vs CT current sensing")
\t\t(comment 2 "Key differences: Zth=66 Ohm (Rw||R16) vs no burden, TVS parasitic values")
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

    with open("combined_bias_divider.kicad_sch", "w") as f:
        f.write(header + "\n")
        for part in parts:
            f.write(part + "\n")
        f.write(footer + "\n")

    print("Generated combined_bias_divider.kicad_sch")


if __name__ == "__main__":
    main()
