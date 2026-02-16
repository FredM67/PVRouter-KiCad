# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PVRouter-KiCad is a KiCad 9.0 hardware design project for the **Mk2 PV Router** -- an open-source 3-phase solar PV diverter system (inspired by www.mk2pvrouter.co.uk). The mainboard is currently at **revision 6.0**.

This is a pure KiCad project with no build system, CI/CD, or scripting. All design work is done in KiCad directly.

## Repository Structure

```
mainboard/           # Primary universal mainboard (3phaseDiverter) -- the main design
3-phase/             # 3-phase variant (older/alternate version with its own schematic+PCB)
1-phase/             # 1-phase variant (schematic only, no PCB)
output_stage/        # Output power stage board (separate PCB)
expansion_boards/
  ESP32/             # ESP32 expansion module
  mk2Wifi/           # WiFi expansion module
KiCad/               # Shared custom libraries
  symbols/           # Custom symbol libraries (.kicad_sym)
  UserDef.pretty/    # Custom footprints for this project
  Library.pretty/    # Additional custom footprints
  3dmodels/          # 3D STEP models for components
```

## Key Design Files

The **mainboard** is the primary active design:
- `mainboard/3phaseDiverter.kicad_pro` -- project file
- `mainboard/3phaseDiverter.kicad_sch` -- schematic
- `mainboard/3phaseDiverter.kicad_pcb` -- PCB layout
- `mainboard/3phaseDiverter.kicad_dru` -- design rules
- `mainboard/UserDef.kicad_sym` -- board-local custom symbols
- `mainboard/production/` -- fabrication-ready output files

## Custom Libraries

Libraries are referenced via `${KIPRJMOD}/../KiCad/` in `fp-lib-table` and `sym-lib-table` files. Some boards also have local `UserDef.kicad_sym` files for board-specific symbols.

Notable custom symbols: ZMPT101B (AC voltage sensor), GDT28H-300-B (gas discharge tube), 2093-300-SM-RPLF.

## Working with KiCad Files

- KiCad files (.kicad_sch, .kicad_pcb, .kicad_sym, .kicad_mod) are S-expression text format and can be read/edited as text, but care must be taken to preserve the S-expression structure.
- The `mainboard/database/project.db` is a binary SQLite database -- do not edit as text.
- When modifying schematic or PCB files, maintain consistency between them (net names, component references).
- The PCB uses multiple net classes with specific clearance and track width rules:

| Net Class | Voltage Domain | Purpose | Notes |
|-----------|---------------|---------|-------|
| **Surge** | Raw mains + transients | PWR1 connector pins, GDT pads, fuse pads, Earth | Highest clearance requirements |
| **HV** | Mains (post-protection) | L1/L2/L3_VOLTAGE, NEUTRAL, PS1 AC pins | 2.5mm clearance to LV nets |
| **HV Divider** | Divider midpoints | Nets between HV resistors and sensing resistors (Net-(R10-Pad2) through Net-(R33-Pad2)) | 1.0mm clearance to HV, 2.5mm to LV -- bridges HV/LV through rated components |
| **Power** | 5V/3.3V DC | +5V, +3.3V, GND, VCC | |
| **Low Power** | Analog/signal | VREF, AVCC, op-amp nets | |
| **CT** | Low voltage | Current transformer signals | |
| **ANT** | RF | SMA connector to RFM69 module (~8mm trace) | 50-ohm target, short enough that impedance matching is not critical |
| **Gnd** | Analog ground | AGND | |
| **Default** | Low voltage | General signals | |

- HV clearance rules are defined in `mainboard/3phaseDiverter.kicad_dru` and are based on IPC-2221 for 230V RMS / 325V peak on uncoated FR4. The board is designed for use inside a Schneider Electric Thalassa enclosure.
- The `3-phase/` directory is obsolete and should be ignored.

## Git Conventions

- Branch: `main`
- The `.gitignore` excludes KiCad backup/autosave files, netlists, autorouter files, and exported BOMs.
- Fabrication output goes in `mainboard/production/`.
