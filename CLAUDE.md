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
  ESP32/             # ESP32 expansion module (obsolete)
  mk2Wifi/           # WiFi expansion module (older, ESP32-based)
  mk2Wifi-C6/        # WiFi/BLE expansion module (active, ESP32-C6)
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

## Key Components (Mainboard)

- **IC1**: ATmega328P (3.3V, 16 MHz) -- microcontroller
- **PS1**: Multicomp Pro MPC10-5 -- AC-DC power supply (10W, 5V/2A)
- **U1**: AP7361C-33E -- 3.3V LDO regulator (1A, SOT-223)
- **U2**: LMV321A -- op-amp, 1.1V AREF buffer (SOT-23-5)
- **RF1**: RFM69CW -- ISM radio module (433/868 MHz)
- **VT1--VT3**: ZMPT101K -- AC voltage transformers
- **CT1--CT3**: Current transformer connectors (YHDC 100A/50mA)
- **GDT1**: 2093-300-SM-RPLF -- gas discharge tube (surge protection)

## Custom Libraries

Libraries are referenced via `${KIPRJMOD}/../KiCad/` in `fp-lib-table` and `sym-lib-table` files. Some boards also have local `UserDef.kicad_sym` files for board-specific symbols.

Notable custom symbols: ZMPT101B (AC voltage sensor), GDT28H-300-B (gas discharge tube), 2093-300-SM-RPLF.

## Working with KiCad Files

- KiCad files (.kicad_sch, .kicad_pcb, .kicad_sym, .kicad_mod) are S-expression text format and can be read/edited as text, but care must be taken to preserve the S-expression structure.
- The `mainboard/database/project.db` is a binary SQLite database -- do not edit as text.
- When modifying schematic or PCB files, maintain consistency between them (net names, component references).
- The PCB uses multiple net classes with specific clearance and track width rules:

| Net Class | Track Width | Voltage Domain | Purpose | Notes |
|-----------|------------|---------------|---------|-------|
| **Surge** | 2.0mm | Raw mains + transients | PWR1 connector pins, GDT pads, fuse pads | Highest clearance requirements |
| **Earth** | 1.3mm | Protective earth | PE conductor | 1.5mm clearance to HV/LV nets |
| **HV** | 1.3mm | Mains (post-protection) | L1/L2/L3_VOLTAGE, NEUTRAL, PS1 AC pins | 1.5mm to LV, 2.0mm inter-phase |
| **HV Divider** | 0.5mm | Divider midpoints | Nets between HV resistors and sensing resistors | 0.8mm to HV, 1.5mm to LV |
| **Power** | 1.0mm | 5V/3.3V DC | +5V, +3.3V, VCC | |
| **ADC** | 0.5mm | Low voltage analog | CT sensing and ZMPT secondary nets | Sensitive analog signals to ADC |
| **Low Power** | 0.5mm | Analog/signal | VREF, AVCC, op-amp nets | |
| **ANT** | 1.0mm | RF | SMA connector to RFM69 module (~8mm trace) | 50-ohm target, short enough that impedance matching is not critical |
| **Gnd** | 0.5mm | Ground | GND, AGND | |
| **Default** | 0.25mm | Low voltage | General signals | |

- HV clearance rules are defined in `mainboard/3phaseDiverter.kicad_dru` and are based on IPC-2221 for solder-mask-coated FR4 (relaxed from B2 uncoated toward B3 coated). Key clearances:

| Pair | Voltage | Clearance |
|------|---------|-----------|
| HV/Surge inter-phase (L1↔L2↔L3) | 565V peak | 2.0mm |
| HV/Surge phase-to-neutral | 325V peak | 1.5mm |
| HV/Surge to LV | 325V peak | 1.5mm |
| Earth to HV/Surge/LV | 325V peak | 1.5mm |
| HV to Surge (same domain) | -- | 1.2mm |
| HV to HV Divider | ~150V peak | 0.8mm |
| HV Divider/Surge to LV | 325V peak | 1.5mm |

  All HV clearance rules exclude pad-to-pad (component pin spacing is manufacturer-rated).
- The board is designed for use inside a Schneider Electric Thalassa enclosure.
- The `3-phase/` directory is obsolete and should be ignored.

## Mainboard PCB Layout

The board is organized in four horizontal zones (Y increases downward):

| Zone | Y range | Contents |
|------|---------|----------|
| **Top edge** | < 35mm | Output connectors (J2–J5, J10–J13), RESET header |
| **Upper (LV)** | 35–65mm | CN1 (SMA), RF1 (RFM69CW), U1 (LDO), IC1 (ATmega328P), U2 (op-amp), ADC TVS diodes |
| **Middle (Analog)** | 65–95mm | CT1–CT3 connectors, bias dividers, coupling caps, voltage sensing |
| **Lower (HV)** | > 95mm | PS1 (MPC10-5, left), fuses, MOVs, CM choke, GDTs, PWR1 (mains connector, right) |

Key layout characteristics:
- HV/LV separation: ~83mm between mains connector and MCU
- IC1 decoupling: dedicated 100nF bypass cap within 3mm of each power pin (VCC, AVCC, AREF)
- Ground stitching: 142 GND + 79 GNDA vias, dense near IC1 (within 2mm of ground pins)
- RF antenna trace: ~8mm from CN1 (SMA) to RF1, well under λ/10 at 868MHz
- Analog channels: CH1/CH2 compact (16–20mm span), CH3 longer (~44mm) due to CT3 position

## mk2Wifi-C6 Expansion Board

The **mk2Wifi-C6** is the active WiFi/BLE expansion module (`expansion_boards/mk2Wifi-C6/`):
- `mk2Wifi-C6.kicad_pro` / `.kicad_sch` / `.kicad_pcb` -- project files
- Rev v1.0, 2-layer, 51.1 × 26.4 mm, all SMD (except J3 UART header)

### Key Components

- **U1**: ESP32-C6-MINI-1/U -- WiFi 6 / BLE 5 / Zigbee / Thread
- **U2**: AP2112K-3.3 -- 3.3V LDO (600mA, SOT-23-5)
- **J2**: USB-C 16P receptacle (USB 2.0)
- **J3**: UART_EXT 1×6 pin socket (mainboard connection, B.Cu)
- **J4**: OLED Molex 1×4 (I2C display)
- **JP1--JP5**: Solder jumpers for GPIO D5--D9 configuration

### PCB Layout

Three horizontal zones (Y increases downward):

| Zone | Y range | Contents |
|------|---------|----------|
| **Top** | 42–48mm | Solder jumpers (JP1–JP5), GPIO series resistors (R5–R9) |
| **Middle** | 48–58mm | U1 (ESP32-C6), decoupling caps (C1, C4), pull resistors |
| **Bottom** | 58–68mm | U2 (LDO), USB-C (J2), OLED (J4), USB CC resistors, LED, button, UART header |

Key layout characteristics:
- Decoupling: all caps within 1.7mm of target pins (C1→U1 1.5mm, C2→U2 out 1.7mm, C5→U2 in 1.7mm)
- Ground stitching: 57 GND vias on 51×26mm board, 9 GND sub-pads under U1 exposed pad
- Powered from mainboard +5V via UART_EXT header

## Output Stage Board

The **output stage** is the triac power switching board (`output_stage/`):
- `Output_stage.kicad_pro` / `.kicad_sch` / `.kicad_pcb` -- project files
- Rev 2.0, 2-layer (routing on B.Cu only), 63.1 × 28.1 mm, all THT

### Key Components

- **Q1**: BTA41-600B -- 41A/600V power triac (TO-218-3, requires external heatsink)
- **U1**: MOC3043M -- zero-crossing opto-triac isolator (DIP-6 socket, 7.5kV isolation)
- **J1**: Phoenix 3-pin -- mains connector (LINE/S_LINE/LOAD)
- **J2, J3**: Molex 2-pin -- control/LED inputs from mainboard
- **R1**: 220Ω -- opto LED current limiter (LV side)
- **R2**: 330Ω -- triac gate resistor (HV side)
- **R3**: 360Ω -- snubber/gate resistor (HV side)

### PCB Layout

- HV side (left): Q1 triac, J1 mains connector, R2, R3
- LV side (right): J2/J3 control connectors, R1
- U1 (MOC3043M) at center-right: galvanic isolation boundary (7.62mm HV/LV pin spacing)
- Copper zones on B.Cu carry main current for LINE and S/LINE nets
- No vias, no SMD -- simple single-layer routing with copper pour

## Git Conventions

- Branch: `main`
- The `.gitignore` excludes KiCad backup/autosave files, netlists, autorouter files, and exported BOMs.
- Fabrication output goes in `mainboard/production/`.
