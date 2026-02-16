**[Français](Readme.md)** | English

# PVRouter-KiCad

KiCad design files for the **Mk2 PV Router** — an open-source universal solar PV diverter system (single-phase, 3-phase with or without neutral, split-phase).

Inspired by [www.mk2pvrouter.co.uk](https://www.mk2pvrouter.co.uk), this project provides the schematics and PCB layouts needed to build a PV router capable of diverting surplus solar generation to resistive loads (water heaters, radiators, etc.).

![Mainboard](mainboard/3phaseDiverter.png)

## Repository structure

| Directory | Description | Status |
|-----------|-------------|--------|
| [`mainboard/`](mainboard/) | Universal mainboard (3phaseDiverter) — rev. 6.0 | Active design |
| [`output_stage/`](output_stage/) | Output power stage (separate PCB) | Active design |
| [`expansion_boards/mk2Wifi/`](expansion_boards/mk2Wifi/) | WiFi/BLE expansion module (ESP32-C3) | Active design |
| [`1-phase/`](1-phase/) | Single-phase variant (schematic only, no PCB) | Obsolete — still sold |
| [`3-phase/`](3-phase/) | 3-phase variant (older version) | Obsolete — still sold |
| [`KiCad/`](KiCad/) | Shared custom libraries (symbols, footprints, 3D models) | — |

## Mainboard

The mainboard is the core of the project. It is a universal design supporting single-phase, 3-phase (with or without neutral), and split-phase configurations. Depending on the configuration, up to 3 current transformers (CTs) are needed. It includes:

- ATmega328P microcontroller
- Up to 3 current sensors (current transformers)
- Up to 3 voltage sensors (ZMPT101B)
- RFM69 radio module (433 MHz)
- On-board power supply from mains
- Surge protection (GDT + fuses)
- Expansion connectors (TRIG_EXT, UART_EXT)

The board is designed to be mounted in a Schneider Electric Thalassa enclosure.

## Expansion modules

- **[mk2Wifi](expansion_boards/mk2Wifi/)** — WiFi/BLE module based on ESP32-C3-MINI-1, with USB-C connector, optional OLED display and DS18B20 temperature sensor

## Output power stage

The **[output power stage](output_stage/)** is a separate board that handles switching of resistive loads via triacs or solid-state relays (SSR).

## Required tools

- [KiCad 9.0](https://www.kicad.org/) or higher
- Custom libraries are included in the `KiCad/` directory and referenced automatically via `fp-lib-table` and `sym-lib-table` files

## Links

- Reference site: [www.mk2pvrouter.co.uk](https://www.mk2pvrouter.co.uk)
- GitHub: [github.com/FredM67/PVRouter-KiCad](https://github.com/FredM67/PVRouter-KiCad)
