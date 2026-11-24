**[Français](Readme.md)** | English

# 3phaseDiverter — Universal mainboard for the Mk2 PV Router

Universal mainboard for the Mk2 PV Router (rev. 6.0). Supports single-phase and 3-phase (with or without neutral) configurations.

## Overview

The 3phaseDiverter board is the core of the Mk2 PV Router system -- an open-source solar PV diverter capable of driving up to three loads based on surplus solar production. It is designed to be housed in a Schneider Electric Thalassa enclosure.

Key features:
- **ATmega328P** microcontroller (16 MHz, DIP-28)
- Up to 3 voltage sensors (**ZMPT101K** transformers, 1000:1000 ratio)
- Up to 3 current transformers (**CT1--CT3** connectors)
- **RFM69CW** radio module (433/868 MHz ISM band) with SMA connector
- On-board AC-DC power supply (**Multicomp Pro MPC10-5**, 5V/10W)
- **AP7361C-33E** LDO regulator (5V to 3.3V, 1A)
- Surge protection: fuses, phase-to-neutral IsoMOV varistors, common-mode choke; optional varistor + GDT pairs to earth
- 1.1V internal AREF buffered by **LMV321A** op-amp, per-channel DC bias to VREF/2
- Expansion connectors: **TRIG_EXT**, **UART_EXT**, **FTDI**, **OLED**
- IPC-2221 compliant design for 230V RMS / 325V peak on uncoated FR4

## Board images

| Front (fully assembled) | Back |
|:-:|:-:|
| ![Front](assets/3phaseDiverter-front.png) | ![Back](assets/3phaseDiverter-back.png) |

| SMD components only | Bare board layout |
|:-:|:-:|
| ![SMD](assets/3phaseDiverter-smd.png) | ![Bare](assets/3phaseDiverter-bare.png) |

## Schematic

[![3phaseDiverter schematic](assets/3phaseDiverter-schematic.svg)](assets/3phaseDiverter-schematic.pdf)

## Design files

| File | Description |
|------|-------------|
| `3phaseDiverter.kicad_pro` | KiCad 9 project file |
| `3phaseDiverter.kicad_sch` | Schematic |
| `3phaseDiverter.kicad_pcb` | PCB layout |
| `3phaseDiverter.kicad_dru` | Design rules |
| `UserDef.kicad_sym` | Board-local custom symbol library |
| `sym-lib-table` | Symbol library table |
| `fp-lib-table` | Footprint library table |

## Bill of Materials

### ICs and modules

| Ref | Value | Package | Description |
|-----|-------|---------|-------------|
| IC1 | ATmega328P | DIP-28 | Microcontroller (16 MHz) |
| U2 | LMV321A | SOT-23-5 | Single op-amp (1.1V AREF buffer) |
| U1 | AP7361C-33E | SOT-223 | 3.3V LDO regulator (1A) |
| PS1 | MPC10-5 | Converter_ACDC_MULTICOMP_PRO | AC-DC power supply module (5V, 10W, Multicomp Pro) |
| RF1 | RFM69CW | Custom | ISM band radio module (433/868 MHz) |

### Voltage sensors

| Ref | Value | Package | Description |
|-----|-------|---------|-------------|
| TR1 | ZMPT101K | Custom | L1 voltage transformer (1000:1000) |
| TR2 | ZMPT101K | Custom | L2 voltage transformer (1000:1000) |
| TR3 | ZMPT101K | Custom | L3 voltage transformer (1000:1000) |

### Protection

| Ref | Value | Package | Description |
|-----|-------|---------|-------------|
| FS0--FS3 | 1A x 250V | THT (Littelfuse 395 series footprint), soldered, no holder | Fuses (4x, one per phase + neutral) |
| GM1--GM3 | 320V | THT (IsoM3300BL2) | Hybrid varistors (MOV + GDT in one package), phase to neutral (3x) |
| RV0--RV3 | 300V | THT, radial (MOV14D471K) | Varistors, each in series with the GDT of the same number, conductor to earth (4x, **optional**) |
| GDT0--GDT3 | 2093-300-SM-RPLF | SMD | Gas discharge tubes, in series with RV0--RV3 (4x, **optional**, soldered by the user) |
| FL1 | RN214-0.3-02-47M | THT (Schaffner RNx14) | Common-mode choke in front of PS1 |
| D1 | SMBJ7.0A | SMB | TVS diode across the 5V rail |
| D11 / D21 / D31 | DF2B7AE | SOD-523 | TVS diodes on the voltage ADC inputs (A0, A2, A4') |
| D12 / D22 / D32 | DF2B7AE | SOD-523 | TVS diodes on the current ADC inputs (A1, A3, A5') |
| D13 / D23 / D33 | CDSOD323-T03C | SOD-323, footprint with two extra through-holes (P12.70mm) | Bidirectional TVS diodes across the CT inputs; the two through-holes take the axial burden resistor of a current-output CT |

RVx and GDTx only work as a pair: the varistor and the GDT are in series between a conductor and earth.

### Connectors

| Ref (silkscreen) | Value | Package | Description |
|------------------|-------|---------|-------------|
| PWR1 | Conn_01x05_PWR | Phoenix Contact MSTBV 2.5 | Mains input (1x5, 5.08mm pitch) |
| TRIG_EXT0 (TRIG_EXT) | Conn_01x06 | Pin header 1x06 2.54mm | Trigger/GPIO header (mk2Wifi) |
| JP8 (UART_EXT) | Conn_01x06 | Pin header 1x06 2.54mm | UART + DS18B20 header (mk2Wifi) |
| J0 (FTDI) | FTDI | Molex SL 1x06 2.54mm | Programming/debug connector |
| J1 (RESET) | RESET | Molex SL 1x02 2.54mm | Reset push-button (GND, /DTR) |
| J31 (OLED) | OLED | Molex SL 1x04 2.54mm | I2C display connector |
| J32, J33 (DS18B20) | DS18B20 | Molex SL 1x03 2.54mm | Temperature sensors (GND, data, +5V) |
| J2--J13 (D2--D13) | -- | Molex SL 1x03 2.54mm | Digital pins: GND, Dx, +5V (only when JP40 is closed) |
| J16--J27 (D2--D13) | -- | Molex SL 1x02 2.54mm | Digital pins: GND, Dx |
| CT1--CT3 | Conn_01x02 | Molex SL 1x02 2.54mm | Current transformer inputs (L1, L2, L3) |
| CN1 | SMA | Amphenol 132291-12, vertical | 50 ohm RF antenna connector |

### Passives -- per-phase blocks (x3)

Each phase (L1/L2/L3) has an identical set of components. Numbering follows the pattern 1xx = L1, 2xx = L2, 3xx = L3.

| Ref (L1 / L2 / L3) | Value | Package | Description |
|----------------------|-------|---------|-------------|
| R10--R15 / R20--R25 / R30--R35 | 20K | 1206 | ZMPT101K primary series resistors (6x in series per phase, converts mains voltage to ~2mA) |
| R16 / R26 / R36 | 150R | 0603 SMD or THT (R_PTH_SMD footprint) | ZMPT101K burden resistor (converts 2mA output to voltage); the mixed footprint takes a second resistor in parallel |
| R17 / R27 / R37 | 1K | 0603 | Series resistor to the voltage ADC input (A0, A2, A4') |
| R19 / R29 / R39 | 1K | 0603 | Series resistor to the current ADC input (A1, A3, A5') |
| R18 / R28 / R38 (schematic only) | depends on the CT | Axial, in the two through-holes of the D13 / D23 / D33 footprint | Burden resistor of a current-output CT; not fitted, soldered by the user when needed |
| R101--R104 / R201--R204 / R301--R304 | 10K | 0603 | 50/50 dividers for VREF/2 bias (1 pair per V and I channel) |
| C10 / C20 / C30 | 10uF | 0603 | Inline AC coupling, voltage channel (series between ZMPT101K burden and V bias junction — blocks DC, passes AC signal) |
| C12 / C22 / C32 | 10uF | 0603 | Inline AC coupling, current channel (series between CT and I bias junction — blocks DC, passes AC signal) |
| C11, C13 / C21, C23 / C31, C33 | 100nF | 0603 | Bypass capacitors, bias junction to AGND (C11/C21/C31 voltage, C13/C23/C33 current) |
| D11, D12 / D21, D22 / D31, D32 | DF2B7AE | SOD-523 | TVS diodes on the ADC inputs (D11/D21/D31 voltage, D12/D22/D32 current) |
| D13 / D23 / D33 | CDSOD323-T03C | SOD-323 + 2 through-holes | Bidirectional TVS diode across the CT input; the through-holes take the burden resistor |

### Passives -- common components

| Ref | Value | Package | Description |
|-----|-------|---------|-------------|
| C1 | 1uF 310VAC | Film, THT | X2 mains capacitor across L1 and neutral, in front of FL1 |
| C3 | 220uF 16V | SMD electrolytic 6.3x7.7 | 5V output filtering |
| C2, C40 | 1uF | 0603 | 5V filtering |
| C41 | 4.7uF | 0603 | U1 output filtering |
| C42 | 100nF | 0603 | U1 output bypass |
| C44 | 10uF | 0603 | VCC (+3.3V net) filtering |
| C4 | 100nF | 0603 | VCC bypass |
| C6, C43 | 100nF | 0603 | AVCC bypass |
| C5 | 100nF | 0603 | AREF bypass |
| C45 | 100nF | 0603 | RFM69CW supply bypass (after FB2) |
| C9 | 100nF | 0603 | /DTR to RESET coupling (auto-reset) |
| C7, C8 | 22pF | 0603 | Crystal load capacitors |
| X1 | 16 MHz | HC-49/U, THT | Crystal |
| R3 | 1M | 0603 | /DTR pull-up |
| R4 | 47K | 0603 | RESET pull-up |
| R6 | 4.7K | 0603 | DS18B20 pull-up |
| R40--R42 | 22R | 0603 | SPI series resistors (to RFM69CW) |
| R43 | 2K2 | 0603 | LED40 resistor |
| R44 | 4K7 | 0603 | LED41 resistor |
| R45 | 47K | 0603 | RFM69CW NSS pull-up |
| FB1 | Ferrite | 0603 | VCC to AVCC filtering |
| FB2 | Ferrite | 0603 | VCC to RFM69CW supply filtering |
| LED40 | ON | 0603 | VCC present |
| LED41 | +5V | 0603 | +5V present on pin 3 of J2--J13 (JP40 closed) |

### Configuration

| Ref (silkscreen) | Type | Description |
|------------------|------|-------------|
| JP0 (V sel.) | SolderJumper 3-pole | ATmega328P supply (VCC): 3.3V from U1 (factory) or 5V |
| JP1 (SDA) | SolderJumper 3-pole | A4 selection: L3 voltage sensing or I2C SDA |
| JP2 (SCL) | SolderJumper 3-pole | A5 selection: L3 current sensing or I2C SCL |
| JP3 (IRQ) | SolderJumper 2-pole | Connects the RFM69CW interrupt to D2 (close when the RF module is used) |
| JP4 (TEMP) | SolderJumper 3-pole | DS18B20 handled by the router (D3) or by the mk2Wifi module |
| JP40 (+5V Rail) | SolderJumper 2-pole | Puts +5V on pin 3 of the digital connectors J2--J13 |
| JP41 (NSS) | SolderJumper 2-pole | Connects the RFM69CW chip select to D10 (close when the RF module is used) |
| GND_LINK1 (GND_LINK) | Wire jumper, 0.75mm2 | Links the low-voltage GND to protective earth (open by default) |
| NT0 | Net tie | Permanent GND--AGND link |

### Test points

| Ref | Net |
|-----|-----|
| TP2 | VREF |
| TP3 | VCC (+3.3V net, ATmega328P supply) |
| TP41 | U1 output (3.3V) |
| TP4 | +5V |
| TP5, TP42 | GND |

### Mounting

| Ref | Description |
|-----|-------------|
| H1--H4 | Mounting holes with pads |

## Connector pinouts

### PWR1 -- Mains input (1x5 Phoenix Contact)

| Pin | Signal |
|-----|--------|
| 1 | Earth |
| 2 | Neutral |
| 3 | L1 |
| 4 | L2 |
| 5 | L3 |

In single-phase mode, a 3-way connector variant is provided (Earth, Neutral, L1).

### TRIG_EXT -- Trigger/GPIO (1x6 pin header)

| Pin | Signal |
|-----|--------|
| 1 | GND |
| 2 | D8 |
| 3 | D7 |
| 4 | D6 |
| 5 | D5 |
| 6 | D9 |

### UART_EXT -- UART + DS18B20 (1x6 pin header)

| Pin | Signal |
|-----|--------|
| 1 | GND |
| 2 | DS18B20 |
| 3 | +5V |
| 4 | RX |
| 5 | TX |
| 6 | DTR |

Signal names (TX, RX) are from the **mainboard's** perspective: TX carries data transmitted by the ATmega328P, RX carries data received.

### FTDI -- Programming/debug (1x6 Molex SL)

| Pin | Signal |
|-----|--------|
| 1 | GND |
| 2 | CTS (NC) |
| 3 | VCC (NC) |
| 4 | TXO |
| 5 | RXI |
| 6 | DTR |

Compatible with standard FTDI adapter pinout. TXO (adapter-to-MCU data) connects to the RX net. RXI (MCU-to-adapter data) connects to the TX net. The DTR signal enables auto-reset for Arduino bootloader uploads.

### OLED -- I2C display (1x4 Molex SL)

| Pin | Signal |
|-----|--------|
| 1 | GND |
| 2 | AVCC |
| 3 | SCL |
| 4 | SDA |

The I2C bus is shared on ATmega328P pins A4 (SDA) and A5 (SCL). In 3-phase mode, these pins are assigned to L3 voltage/current sensing -- the OLED display is then unavailable. Selection is made via solder jumpers **JP1** and **JP2**.

### CT1 / CT2 / CT3 -- Current transformers (1x2 Molex SL)

| Pin | Signal |
|-----|--------|
| 1 | CT signal |
| 2 | AGND |

CT1 is used in both single-phase and 3-phase mode. In 3-phase mode, CT2 and CT3 measure L2 and L3. In single-phase mode, CT2 (A3) remains fully usable, for instance to measure the diverted current; CT3 is not available when JP2 routes A5 to I2C SCL.

### CN1 -- RF antenna (SMA)

Vertical SMA female jack (Amphenol 132291-12) for a 50 ohm antenna. Connected to the RFM69CW module via an approximately 8mm trace. The trace is short enough that impedance matching is not critical.

## ATmega328P pin mapping

### Analog inputs

| Arduino Pin | Port | Function | Notes |
|-------------|------|----------|-------|
| A0 | PC0 | L1 voltage sensing | Via resistive divider + ZMPT101K |
| A1 | PC1 | L1 current sensing | Via CT1 |
| A2 | PC2 | L2 voltage sensing | Via resistive divider + ZMPT101K |
| A3 | PC3 | L2 current sensing | Via CT2 |
| A4 | PC4 | L3 voltage sensing / I2C SDA | Selected by JP1 |
| A5 | PC5 | L3 current sensing / I2C SCL | Selected by JP2 |

### Digital outputs and communication

| Arduino Pin | Port | Function | Notes |
|-------------|------|----------|-------|
| D0 | PD0 | UART RX | Serial receive (FTDI, UART_EXT) |
| D1 | PD1 | UART TX | Serial transmit (FTDI, UART_EXT) |
| D2 | PD2 | RFM69CW interrupt | INT0, through JP3 |
| D3 | PD3 | DS18B20 (1-Wire) | Temperature sensor, when JP4 set to router |
| D4 | PD4 | Digital input | General purpose |
| D5 | PD5 | Trigger output | TRIG_EXT pin 5 |
| D6 | PD6 | Trigger output | TRIG_EXT pin 4 |
| D7 | PD7 | Trigger output | TRIG_EXT pin 3 |
| D8 | PB0 | Trigger output | TRIG_EXT pin 2 |
| D9 | PB1 | Trigger output | TRIG_EXT pin 6 |
| D10 | PB2 | SPI SS | RFM69CW chip select, through JP41 |
| D11 | PB3 | SPI MOSI | Data to RFM69CW |
| D12 | PB4 | SPI MISO | Data from RFM69CW |
| D13 | PB5 | SPI SCK | SPI clock |

## Power supply

### Power chain

Mains power enters through the **PWR1** connector:

```
PWR1 -> Fuses (FS0-FS3), one per conductor
     -> GM1-GM3 between each phase and neutral
     -> optional RVx + GDTx pairs between each conductor and earth
     -> C1 (X2) across L1 and neutral -> Common-mode choke (FL1)
     -> PS1 (MPC10-5): 230VAC -> 5VDC, 10W
     -> +5V rail (C2, C3, C40; D1 SMBJ7.0A TVS)
     -> U1 (AP7361C-33E): 5V -> 3.3V
     -> JP0 (V sel.): VCC = U1 output (factory) or +5V
```

The voltage sensing branches (L1/L2/L3_SENSING) start after the fuses.

### Power rails

| Rail | Voltage | Usage |
|------|---------|-------|
| +5V | 5V | PS1 output; UART_EXT pin 3 (mk2Wifi), DS18B20 connectors, pin 3 of J2--J13 through JP40, U1 input |
| U1 output | 3.3V | Goes to VCC through JP0 (factory position); TP41 |
| VCC (+3.3V net) | 3.3V (5V if JP0 is moved) | ATmega328P, RFM69CW (through FB2), pull-ups, LED40 |
| AVCC | VCC filtered by FB1 | ATmega328P AVCC, LMV321A, OLED connector |
| VREF | 1.1V | Internal reference (AREF) buffered by the LMV321A |
| GND | 0V | Ground |
| AGND | 0V | Analog ground, tied to GND by the net tie NT0 |
| Earth | -- | Protective earth (PWR1 pin 1); linked to GND only if GND_LINK is closed |

### Decoupling

- C1 (1uF 310VAC, X2): mains-side filtering, across L1 and neutral
- C3 (220uF), C2, C40 (1uF): 5V filtering
- C41 (4.7uF), C42 (100nF): U1 output
- C44 (10uF), C4 (100nF): VCC
- C6, C43 (100nF): AVCC; C5 (100nF): AREF
- C45 (100nF): RFM69CW supply
- C7, C8 (22pF): crystal load capacitors for X1
- FB1, FB2 (ferrites): AVCC and RFM69CW supply filtering

## Resistor power dissipation

The ADC reference voltage is the ATmega328P internal 1.1V reference, buffered by the LMV321A. The ADC range is therefore 0--1.1V, with a DC bias at the midpoint VREF/2 = 0.55V.

### ZMPT101K primary chain (per phase: 6 x 20K = 120K in series)

| Mains voltage | Current (RMS) | Power per 20K resistor | Total (6 resistors) | 1206 utilisation (250mW typ.) |
|---------------|---------------|------------------------|----------------------|-------------------------------|
| 110V | 0.917mA | 16.8mW | 101mW | 7% |
| 230V | 1.917mA | **73.5mW** | 441mW | **29%** |
| 250V | 2.083mA | 86.8mW | 521mW | 35% |

At 230V nominal, the three phases dissipate 3 x 441 = **1.32W** in the divider chains.

### ZMPT101K burden resistor (R16 / R26 / R36 -- 150R)

Secondary current = primary current (1:1 ratio). At 230V: I = 1.917mA.
- P = (1.917mA)^2 x 150 = **0.55mW** -- negligible

### CT burden resistor (R18 / R28 / R38 in the schematic -- 22R example)

Power depends on the CT type and rating.

**Voltage-output CT** (e.g. SCT-013-030, 30A/1V): the burden resistor is built into the CT. No burden resistor is fitted. Dissipation: **negligible**.

**Current-output CT** (e.g. SCT-013-000, 100A/50mA): the secondary current flows through the burden resistor, an axial resistor soldered in the two through-holes of the D13 / D23 / D33 footprint. Dissipation depends on the measured primary current:

| Primary current | I secondary (100A/50mA) | P in 22R | 0.5W axial resistor (DIN0309 size of the footprint) |
|-----------------|-------------------------|----------|---------------------|
| 20A | 10mA | 2.2mW | < 1% |
| 60A | 30mA | 19.8mW | 4% |
| 100A | 50mA | 55mW | 11% |

**Warning:** With a current-output CT, the burden resistor must be sized so the peak voltage does not exceed 0.55V (half the ADC range at VREF = 1.1V). Formula: **R = 0.55V / I_sec_peak**. With 22R, the max peak current is 25mA. The TVS diodes (DF2B7AE) protect the ADC but do not limit current through the burden resistor: if the CT delivers more than expected, the resistor may overheat.

Within the ADC range:
- I_sec_max = 0.55V / 22R = 25mA peak = 17.7mA RMS
- **P = (17.7mA)^2 x 22 = 6.9mW** -- negligible

### VREF/2 bias dividers (R101--R104 / R201--R204 / R301--R304 -- 10K)

Two 10K resistors in series between VREF (1.1V) and GND:
- I = 1.1V / 20K = 55uA
- **P per 10K = 30uW** -- negligible

The 10K value (Thevenin impedance 5K) meets the ATmega328P datasheet recommendation of ≤10K source impedance for the ADC 14pF S/H capacitor. A 100nF bypass capacitor (C11/C13 per phase) from the bias junction to AGND filters high-frequency noise without attenuating the 50Hz signal.

### Other resistors

| Ref | Value | Voltage | Current | Power |
|-----|-------|---------|---------|-------|
| R3 | 1M | 3.3V | 3.3uA | 0.011mW |
| R4 | 47K | 3.3V | 70uA | 0.23mW |
| R6 | 4.7K | 3.3V | 0.70mA | 2.3mW |
| R17 / R27 / R37 | 1K | < 2V | < 2mA | < 4mW |
| R19 / R29 / R39 | 1K | < 1V | < 1mA | < 1mW |
| R40--R42 | 22R | 3.3V | signal | < 5mW |

All resistors outside the ZMPT101K primary chain dissipate less than 5mW. Only **R10--R15 / R20--R25 / R30--R35** have significant dissipation (73.5mW each at 230V, i.e. 29% of a 250mW 1206 resistor).

## Surge protection

The board implements multi-layer protection compliant with IPC-2221 for operation at 230V RMS on uncoated FR4.

### Protection layers

1. **Fuses (FS0--FS3)**: 1A x 250V, one per phase and neutral, soldered directly (no holder). They open on a short circuit on the board, for example a varistor at end of life or a failed PS1 or C1.
2. **Hybrid varistors (GM1--GM3)**: IsoMOV (MOV + GDT in one package), 320V, between each phase and neutral, after the fuses.
3. **Optional RVx + GDTx pairs (RV0--RV3, GDT0--GDT3)**: for full lightning protection. Each varistor is in series with the GDT of the same number, between a conductor and earth: RV0 + GDT0 on neutral, RV1 + GDT1 on L1, RV2 + GDT2 on L2, RV3 + GDT3 on L3. Not fitted by default; the user solders them, always as a pair.
4. **X2 capacitor (C1) and common-mode choke (FL1)**: filter the supply of PS1.
5. **TVS diode (D1, SMBJ7.0A)**: protects the 5V rail at the power supply output.
6. **ADC input TVS diodes**: per phase, a DF2B7AE on the voltage input (D11/D21/D31) and on the current input (D12/D22/D32), and a CDSOD323-T03C across the CT input (D13/D23/D33).

### Voltage domains and net classes

The board uses multiple net classes with specific clearance rules:

| Class | Domain | Usage |
|-------|--------|-------|
| Surge | Raw mains + transients | PWR1 pins, GDT pads, fuse pads, Earth |
| HV | Mains (post-protection) | L1/L2/L3_VOLTAGE, NEUTRAL, PS1 AC side |
| HV Divider | Divider midpoints | Nets between HV resistors and sensing resistors |
| Power | 5V/3.3V DC | +5V, +3.3V, GND, VCC |
| Low Power | Analog/signal | VREF, AVCC, op-amp nets |
| CT | Low voltage | Current transformer signals |
| ANT | RF | SMA connector to RFM69 module (~8mm trace) |
| Gnd | Analog ground | AGND |
| Default | Low voltage | General signals |

HV clearance rules are defined in `3phaseDiverter.kicad_dru`. HV-to-LV clearance is 2.5mm; HV-to-HV Divider clearance is 1.0mm.

## Configuration

### Solder jumpers

See the [Configuration](#configuration) table of the BOM: JP0 (V sel.), JP1 (SDA), JP2 (SCL), JP3 (IRQ), JP4 (TEMP), JP40 (+5V Rail), JP41 (NSS) and the GND_LINK wire jumper (Earth to GND, 0.75mm2 wire).

### Single-phase vs 3-phase

All SMD components are assembled in production regardless of configuration, except the optional gas discharge tubes GDT0--GDT3. Single-phase vs 3-phase selection is done via solder jumpers and connector choice.

In **single-phase** mode, solder jumpers JP1 and JP2 are set to I2C position (SDA/SCL), enabling the OLED display: they come pre-connected to the L3 sensing lines used in 3-phase mode, so that link must be cut and the I2C side bridged. A 3-way PWR1 connector variant is provided (Earth, Neutral, L1). CT1 measures the grid current; CT2 can be connected as well, its input being fully assembled (the single-phase firmware uses it to measure the diverted energy).

In **3-phase** mode, solder jumpers JP1 and JP2 are set to L3 sensing (A4'/A5' position), which disables the OLED display. The 5-way PWR1 connector is used and all three CTs are connected.

## Expansion module integration

The mainboard is designed to accept the **mk2Wifi** expansion module via the TRIG_EXT and UART_EXT connectors:

- The mainboard uses **pin headers** (male); the mk2Wifi uses **pin sockets** (female)
- +5V power is supplied from the mainboard through UART_EXT pin 3
- UART (TX/RX) provides serial communication with the expansion module
- The DS18B20 signal passes through UART_EXT pin 2 for 1-Wire temperature sensing
- GPIO signals D5--D9 provide trigger/control outputs via TRIG_EXT
- The I2C bus (SCL/SDA) is **local to the mk2Wifi module only** -- it connects the ESP32-C6 to the OLED display and is not routed to the mainboard

## Programming

The **FTDI** connector (Molex SL 1x6) allows firmware upload via a USB-to-serial FTDI or compatible adapter:

1. **Connection**: plug the FTDI adapter into connector J0. The pinout is compatible with standard FTDI cables (GND on pin 1). Pin 3 (VCC) is not connected: the adapter does not power the board.
2. **Auto-reset**: the DTR signal triggers an automatic ATmega328P reset through a coupling capacitor, allowing upload without manual intervention.
3. **Environment**: Arduino-compatible (ATmega328P with bootloader). Use the "Arduino Uno" board or equivalent in the Arduino IDE.

### DS18B20 temperature sensor

The 1-Wire DS18B20 sensor is always connected on the mainboard. Solder jumper **JP4** selects which device handles the sensor:
- **Router position**: signal is routed to ATmega328P pin D3
- **mk2Wifi position**: signal is routed to the expansion module via UART_EXT pin 2

The required pull-up resistor is built into the board (R6, 4.7K).
