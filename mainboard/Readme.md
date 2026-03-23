Français | **[English](Readme.en.md)**

# 3phaseDiverter — Carte principale universelle du Mk2 PV Router

Carte principale universelle pour le Mk2 PV Router (rév. 6.0). Elle prend en charge les configurations monophasé, triphasé (avec ou sans neutre) et split-phase.

## Présentation

La carte 3phaseDiverter est le cœur du système Mk2 PV Router — un routeur solaire photovoltaïque open source capable de piloter jusqu'à trois charges selon la production solaire excédentaire. Elle est conçue pour être installée dans un boîtier Schneider Electric Thalassa.

Caractéristiques principales :
- Microcontrôleur **ATmega328P** (16 MHz, DIP-28)
- Jusqu'à 3 capteurs de tension (transformateurs **ZMPT101K**, rapport 1000:1000)
- Jusqu'à 3 transformateurs de courant (connecteurs **CT1–CT3**)
- Module radio **RFM69CW** (bande ISM 433/868 MHz) avec connecteur SMA
- Alimentation AC-DC intégrée (**RAC05E-05SKT**, 5 V / 3 W, Mornsun)
- Régulateur LDO **AP2112K-3.3** (5 V → 3,3 V, 600 mA)
- Protection parafoudre multiniveau (éclateur GDT, fusibles, varistances MOV, selfs de mode commun)
- Buffer de la référence interne 1,1 V (AREF) par amplificateur opérationnel **LMV321A**, polarisation des voies à VREF/2
- Connecteurs d'extension : **TRIG_EXT**, **UART_EXT**, **FTDI**, **OLED**
- Conception conforme IPC-2221 pour 230 V RMS / 325 V crête sur FR4 non revêtu

## Images de la carte

| Face avant (assemblée) | Face arrière |
|:-:|:-:|
| ![Avant](assets/3phaseDiverter-front.png) | ![Arrière](assets/3phaseDiverter-back.png) |

| Composants CMS uniquement | Circuit imprimé nu |
|:-:|:-:|
| ![CMS](assets/3phaseDiverter-smd.png) | ![Nu](assets/3phaseDiverter-bare.png) |

## Schéma

[![Schéma 3phaseDiverter](assets/3phaseDiverter-schematic.svg)](assets/3phaseDiverter-schematic.pdf)

## Fichiers de conception

| Fichier | Description |
|---------|-------------|
| `3phaseDiverter.kicad_pro` | Fichier projet KiCad 9 |
| `3phaseDiverter.kicad_sch` | Schéma |
| `3phaseDiverter.kicad_pcb` | Circuit imprimé |
| `3phaseDiverter.kicad_dru` | Règles de conception |
| `UserDef.kicad_sym` | Bibliothèque de symboles locale |
| `sym-lib-table` | Table des bibliothèques de symboles |
| `fp-lib-table` | Table des bibliothèques d'empreintes |

## Nomenclature (BOM)

### Circuits intégrés et modules

| Réf | Valeur | Boîtier | Description |
|-----|--------|---------|-------------|
| IC1 | ATmega328P | DIP-28 | Microcontrôleur (16 MHz) |
| U2 | LMV321A | SOT-23-5 | Amplificateur opérationnel simple (buffer AREF 1,1 V) |
| U1 | AP2112K-3.3 | SOT-23-5 | Régulateur LDO 3,3 V (600 mA) |
| PS1 | RAC05E-05SKT | HS-40005 | Module d'alimentation AC-DC (5 V, 3 W, Mornsun) |
| RF1 | RFM69CW | Custom | Module radio ISM (433/868 MHz) |

### Capteurs de tension

| Réf | Valeur | Boîtier | Description |
|-----|--------|---------|-------------|
| TR1 | ZMPT101K | Custom | Transformateur de tension L1 (1000:1000) |
| TR2 | ZMPT101K | Custom | Transformateur de tension L2 (1000:1000) |
| TR3 | ZMPT101K | Custom | Transformateur de tension L3 (1000:1000) |

### Protection

| Réf | Valeur | Boîtier | Description |
|-----|--------|---------|-------------|
| GDT0–GDT3 | 2093-300-SM-RPLF | SMD | Éclateurs à gaz (4×, un par phase + neutre) |
| GM1–GM3 | GMOV 320 V | SMD | Varistances combinées GDT+MOV (3×, une par phase) |
| RV0–RV3 | 300 V | Radial | Varistances (4×, une par phase + neutre) |
| D1 | SMBJ7.0A | SMB | Diode TVS (protection alimentation 5 V) |
| D11, D12 | DF2B7AE | SOD-523 | Diodes TVS (protection ADC phase L1) |
| D21, D22 | DF2B7AE | SOD-523 | Diodes TVS (protection ADC phase L2) |
| D31, D32 | DF2B7AE | SOD-523 | Diodes TVS (protection ADC phase L3) |
| D13, D23, D33 | CDSOD323-T03C | SOD-323 | Diodes TVS bidirectionnelles (protection ADC en cas de CT courant sans résistance de charge, une par phase) |
| FS0–FS3 | 1 A × 250 V | Axial | Fusibles (4×, un par phase + neutre) |
| FL1 | RN214-0.3-02-47M | Custom | Self de mode commun (Schaffner) |

### Connecteurs

| Réf | Valeur | Boîtier | Description |
|-----|--------|---------|-------------|
| PWR1 | Conn_01x05_PWR | Phoenix Contact MSTBV 2,5 | Entrée secteur triphasé (1×5, pas 5,08 mm) |
| TRIG_EXT | Conn_01x06 | PinHeader 1×06 2,54 mm | Connecteur déclenchement/GPIO |
| UART_EXT | Conn_01x06 | PinHeader 1×06 2,54 mm | Connecteur UART + DS18B20 |
| FTDI | Conn_01x06 | Molex SL 1×06 2,54 mm | Connecteur programmation/débogage |
| OLED | Conn_01x04 | Molex SL 1×04 2,54 mm | Connecteur écran I2C |
| CN1 | BU-SMA-V | SMA vertical | Connecteur antenne RF 50 Ω |
| CT1 | Conn_01x02 | Molex SL 1×02 2,54 mm | Entrée transformateur de courant L1 |
| CT2 | Conn_01x02 | Molex SL 1×02 2,54 mm | Entrée transformateur de courant L2 |
| CT3 | Conn_01x02 | Molex SL 1×02 2,54 mm | Entrée transformateur de courant L3 |

### Passifs — blocs par phase (×3)

Chaque phase (L1/L2/L3) possède un ensemble identique de composants. La numérotation suit le schéma 1xx = L1, 2xx = L2, 3xx = L3.

| Réf (L1 / L2 / L3) | Valeur | Boîtier | Description |
|----------------------|--------|---------|-------------|
| R10–R15 / R20–R25 / R30–R35 | 20K | 0805 | Résistances série primaire ZMPT101K (6× en série par phase, conversion tension secteur → ~2 mA) |
| R16 / R26 / R36 | 150R | 0603 | Résistance de charge ZMPT101K (conversion courant 2 mA → tension) ; empreinte double pour ajout en parallèle (réseaux 110 V) |
| R17 / R27 / R37 | 1K | 0603 | Conditionnement de signal |
| R18 / R28 / R38 | 22R typ. | 0603 | Résistance de charge CT courant (valeur selon le calibre du CT) |
| R19 / R29 / R39 | 1K | 0603 | Protection série |
| R101–R104 / R201–R204 / R301–R304 | 10K | 0603 | Diviseurs 50/50 pour polarisation à VREF/2 (1 paire par voie V et I) |
| C10 / C20 / C30 | 10 µF | 0603 | Couplage AC série, voie tension (entre charge ZMPT101K et point de polarisation V — bloque le continu, passe le signal alternatif) |
| C12 / C22 / C32 | 10 µF | 0603 | Couplage AC série, voie courant (entre CT et point de polarisation I — bloque le continu, passe le signal alternatif) |
| C11, C13 / C21, C23 / C31, C33 | 100 nF | 0603 | Condensateurs de découplage, point de polarisation vers AGND (C11/C21/C31 tension, C13/C23/C33 courant) |
| D11, D12 / D21, D22 / D31, D32 | DF2B7AE | SOD-523 | Diodes TVS (protection entrée ADC tension, 2× par phase) |
| D13 / D23 / D33 | CDSOD323-T03C | SOD-323 | Diode TVS bidirectionnelle (protection ADC si CT courant sans résistance de charge R18/R28/R38, 1× par phase) |

### Passifs — composants communs

| Réf | Valeur | Boîtier | Description |
|-----|--------|---------|-------------|
| C1 | 1 µF 310 VAC | Film | Condensateur de filtrage secteur (classe X2) |
| C3 | 120 µF | Électrolytique | Filtrage alimentation |
| C2, C40, C41 | 1 µF | 0603 | Filtrage |
| C4, C5, C6, C9, C42, C43 | 100 nF | 0603 | Découplage CI |
| C7, C8 | 22 pF | 0603 | Condensateurs de charge quartz |
| X1 | 16 MHz | HC-49 | Quartz |
| R3 | 1M | 0603 | Pull-up RESET |
| R4 | 47K | 0603 | Pull-up |
| R6 | 4,7K | 0603 | Pull-up DS18B20 |
| R39–R42 | 22R | 0603 | Terminaison série (SPI) |
| FB1 | Ferrite | 0603 | Perle de ferrite (filtrage alimentation) |

### Configuration

| Réf | Type | Description |
|-----|------|-------------|
| JP0 | SolderJumper 3 pôles | Alimentation ATmega328P : 3,3 V (défaut) ou 5 V |
| JP1 | SolderJumper 3 pôles | Sélection A4 : mesure tension L3 ou I2C SDA |
| JP2 | SolderJumper 3 pôles | Sélection A5 : mesure courant L3 ou I2C SCL |
| JP3 | SolderJumper 2 pôles | Configuration déclenchement |
| JP4 | SolderJumper 3 pôles | DS18B20 géré par le routeur (D3) ou par le module mk2Wifi (libellé « TEMP ») |
| GND_LINK | SolderJumper 2 pôles | Pont GND–AGND (cavalier fil) |

### Montage

| Réf | Description |
|-----|-------------|
| H1–H4 | Trous de fixation avec pastilles |

## Brochage des connecteurs

### PWR1 — Entrée secteur (1×5 Phoenix Contact)

| Broche | Signal |
|--------|--------|
| 1 | Terre |
| 2 | Neutre |
| 3 | L1 |
| 4 | L2 |
| 5 | L3 |

En monophasé, un connecteur 3 voies est fourni (Terre, Neutre, L1).

### TRIG_EXT — Déclenchement/GPIO (1×6 barrette mâle)

| Broche | Signal |
|--------|--------|
| 1 | GND |
| 2 | D8 |
| 3 | D7 |
| 4 | D6 |
| 5 | D5 |
| 6 | D9 |

### UART_EXT — UART + DS18B20 (1×6 barrette mâle)

| Broche | Signal |
|--------|--------|
| 1 | GND |
| 2 | DS18B20 |
| 3 | +5 V |
| 4 | RX |
| 5 | TX |
| 6 | DTR |

Les noms des signaux (TX, RX) sont du point de vue de la **carte principale** : TX transporte les données émises par l'ATmega328P, RX les données reçues.

### FTDI — Programmation/débogage (1×6 Molex SL)

| Broche | Signal |
|--------|--------|
| 1 | GND |
| 2 | CTS (NC) |
| 3 | VCC (NC) |
| 4 | TXO |
| 5 | RXI |
| 6 | DTR |

Brochage compatible avec les adaptateurs FTDI standard. TXO (données de l'adaptateur vers le MCU) est relié au réseau RX. RXI (données du MCU vers l'adaptateur) est relié au réseau TX. Le signal DTR permet l'auto-reset pour le téléversement via le bootloader Arduino.

### OLED — Écran I2C (1×4 Molex SL)

| Broche | Signal |
|--------|--------|
| 1 | GND |
| 2 | VCC |
| 3 | SCL |
| 4 | SDA |

Le bus I2C est partagé sur les broches A4 (SDA) et A5 (SCL) de l'ATmega328P. En mode triphasé, ces broches sont affectées à la mesure de tension/courant L3 — l'écran OLED n'est alors pas disponible. Le choix est effectué par les cavaliers **JP1** et **JP2**.

### CT1 / CT2 / CT3 — Transformateurs de courant (1×2 Molex SL)

| Broche | Signal |
|--------|--------|
| 1 | Signal CT |
| 2 | AGND |

CT1 est utilisé en monophasé et en triphasé. CT2 et CT3 sont utilisés uniquement en triphasé.

### CN1 — Antenne RF (SMA)

Connecteur SMA femelle vertical (Amphenol 132291-12) pour antenne 50 Ω. Relié au module RFM69CW par une piste d'environ 8 mm. La piste est courte, ce qui rend l'adaptation d'impédance non critique.

## Affectation des broches de l'ATmega328P

### Entrées analogiques

| Broche Arduino | Port | Fonction | Notes |
|----------------|------|----------|-------|
| A0 | PC0 | Mesure de tension L1 | Via diviseur résistif + ZMPT101K |
| A1 | PC1 | Mesure de courant L1 | Via CT1 |
| A2 | PC2 | Mesure de tension L2 | Via diviseur résistif + ZMPT101K |
| A3 | PC3 | Mesure de courant L2 | Via CT2 |
| A4 | PC4 | Mesure de tension L3 / I2C SDA | Sélection par JP1 |
| A5 | PC5 | Mesure de courant L3 / I2C SCL | Sélection par JP2 |

### Sorties numériques et communication

| Broche Arduino | Port | Fonction | Notes |
|----------------|------|----------|-------|
| D0 | PD0 | UART RX | Réception série (FTDI, UART_EXT) |
| D1 | PD1 | UART TX | Émission série (FTDI, UART_EXT) |
| D2 | PD2 | Interruption RFM69CW | INT0 |
| D3 | PD3 | DS18B20 (1-Wire) | Capteur de température, si JP4 en position routeur |
| D4 | PD4 | Entrée numérique | Usage général |
| D5 | PD5 | Sortie déclenchement | TRIG_EXT broche 5 |
| D6 | PD6 | Sortie déclenchement | TRIG_EXT broche 4 |
| D7 | PD7 | Sortie déclenchement | TRIG_EXT broche 3 |
| D8 | PB0 | Sortie déclenchement | TRIG_EXT broche 2 |
| D9 | PB1 | Sortie déclenchement | TRIG_EXT broche 6 |
| D10 | PB2 | SPI SS | Sélection du RFM69CW |
| D11 | PB3 | SPI MOSI | Données vers RFM69CW |
| D12 | PB4 | SPI MISO | Données depuis RFM69CW |
| D13 | PB5 | SPI SCK | Horloge SPI |

## Alimentation

### Chaîne d'alimentation

Le secteur entre par le connecteur **PWR1** et traverse une chaîne de protection avant d'atteindre le module d'alimentation :

```
Secteur → GDT (éclateurs) → Fusibles (FS0–FS3) → Varistances (RV0–RV3, GM1–GM3)
       → Self de mode commun (FL1) → Condensateur film (C1)
       → PS1 (RAC05E-05SKT) : 230 VAC → 5 VDC, 3 W
       → D1 (SMBJ7.0A) : protection TVS côté 5 V
       → U1 (AP2112K-3.3) : 5 V → 3,3 V, 600 mA
```

### Rails d'alimentation

| Rail | Tension | Usage |
|------|---------|-------|
| +5 V | 5 V | Connecteurs UART_EXT et FTDI |
| +3,3 V | 3,3 V | ATmega328P, module RFM69CW |
| AVCC | 3,3 V (filtré) | Référence analogique ATmega328P, connecteur OLED |
| VREF | — | Tension de référence analogique |
| GND | 0 V | Masse numérique |
| AGND | 0 V | Masse analogique (reliée à GND par GND_LINK) |

### Découplage

- C1 (1 µF 310 VAC) : filtrage côté secteur
- C3 (120 µF) : filtrage sortie alimentation 5 V
- C2, C41 (1 µF) : filtrage secondaire
- C4, C5, C6, C9, C42, C43 (100 nF) : découplage local des CI
- C7, C8 (22 pF) : condensateurs de charge du quartz X1
- FB1 (ferrite) : filtrage rail d'alimentation

## Dissipation des résistances

La tension de référence ADC est la référence interne 1,1 V de l'ATmega328P, bufferisée par le LMV321A. La plage ADC est donc 0–1,1 V, avec une polarisation au point milieu VREF/2 = 0,55 V.

### Chaîne primaire ZMPT101K (par phase : 6 × 20K = 120K en série)

| Tension secteur | Courant (RMS) | Puissance par résistance 20K | Total (6 résistances) | Taux d’utilisation 0805 (125 mW) |
|-----------------|---------------|------------------------------|-----------------------|------------------------------------------|
| 110 V | 0,917 mA | 16,8 mW | 101 mW | 13 % |
| 230 V | 1,917 mA | **73,5 mW** | 441 mW | **59 %** |
| 250 V | 2,083 mA | 86,8 mW | 521 mW | 69 % |

À 230 V nominal, les trois phases dissipent 3 × 441 = **1,32 W** dans les chaînes de diviseurs.

### Résistance de charge ZMPT101K (R16 / R26 / R36 — 150 R)

Courant secondaire = courant primaire (rapport 1 : 1). À 230 V : I = 1,917 mA.
- P = (1,917 mA)² × 150 = **0,55 mW** — négligeable

### Résistance de charge CT (R18 / R28 / R38 — 22 R typ.)

La puissance dépend du calibre du CT.

**CT à sortie tension** (ex. : SCT-013-030, 30 A/1 V) : la résistance de charge est intégrée dans le CT. R18 n’est pas montée. Dissipation : **négligeable**.

**CT à sortie courant** (ex. : SCT-013-000, 100 A/50 mA) : le courant secondaire traverse R18. La dissipation dépend du courant primaire mesuré :

| Courant primaire | I secondaire (100 A/50 mA) | P dans 22 R | Tenue 0603 (100 mW) |
|------------------|---------------------------------|---------------|------------------------|
| 20 A | 10 mA | 2,2 mW | 2 % |
| 60 A | 30 mA | 19,8 mW | 20 % |
| 100 A | 50 mA | 55 mW | 55 % |

⚠️ **Avec un CT à sortie courant**, la valeur de R18 doit être choisie pour que la tension crête ne dépasse pas 0,55 V (demi-plage ADC à VREF = 1,1 V). Formule : **R = 0,55 V / I_sec_crête**. Avec 22 R, le courant crête max est de 25 mA. Les diodes TVS (DF2B7AE) protègent l’ADC mais ne limitent pas le courant dans la résistance de charge : si le CT délivre plus que prévu, la résistance peut surchauffer.

Dans les limites de la plage ADC :
- I_sec_max = 0,55 V / 22 R = 25 mA crête ≈ 17,7 mA RMS
- **P = (17,7 mA)² × 22 = 6,9 mW** — négligeable

### Diviseurs VREF/2 (R101–R104 / R201–R204 / R301–R304 — 10K)

Deux résistances de 10K en série entre VREF (1,1 V) et GND :
- I = 1,1 V / 20K = 55 µA
- **P par 10K = 30 µW** — négligeable

La valeur de 10K (impédance Thévenin 5K) respecte la recommandation du datasheet ATmega328P (≤ 10K d’impédance source pour le condensateur S/H de 14 pF de l’ADC). Un condensateur de découplage de 100 nF (C11/C13 par phase) entre le point de polarisation et AGND filtre le bruit haute fréquence sans atténuer le signal à 50 Hz.

### Autres résistances

| Réf | Valeur | Tension | Courant | Puissance |
|-----|--------|---------|---------|-----------|
| R3 | 1M | 3,3 V | 3,3 µA | 0,011 mW |
| R4 | 47K | 3,3 V | 70 µA | 0,23 mW |
| R6 | 4,7K | 3,3 V | 0,70 mA | 2,3 mW |
| R17 / R27 / R37 | 1K | < 2 V | < 2 mA | < 4 mW |
| R19 / R29 / R39 | 1K | < 1 V | < 1 mA | < 1 mW |
| R40–R42 | 22R | 3,3 V | signal | < 5 mW |

Toutes les résistances hors chaîne primaire ZMPT101K dissipent moins de 5 mW. Seules les **R10–R15 / R20–R25 / R30–R35** présentent une dissipation significative (73,5 mW chacune à 230 V, soit 59 % de la puissance nominale 0805).

## Protection parafoudre

La carte implémente une protection multiniveau conforme aux normes IPC-2221 pour le fonctionnement à 230 V RMS sur FR4 non revêtu.

### Niveaux de protection

1. **Éclateurs à gaz (GDT0–GDT3)** : première ligne de défense contre les surtensions transitoires. Modèle 2093-300-SM-RPLF, tension d'amorçage 300 V.
2. **Fusibles (FS0–FS3)** : 1 A × 250 V, un par phase et neutre. Limitent le courant en cas de défaut.
3. **Varistances (RV0–RV3, GM1–GM3)** : écrêtage des surtensions résiduelles. Les GM1–GM3 combinent un éclateur et une varistance dans un seul boîtier.
4. **Self de mode commun (FL1)** : filtre les perturbations de mode commun sur les lignes secteur.
5. **Diode TVS (D1, SMBJ7.0A)** : protection du rail 5 V en sortie du module d'alimentation.
6. **Diodes TVS (D11/D12, D21/D22, D31/D32, DF2B7AE)** : protection des entrées ADC du microcontrôleur, trois par phase (2× DF2B7AE pour la tension, 1× CDSOD323-T03C pour le courant en cas de CT sans résistance de charge).

### Domaines de tension et classes de réseau

La carte utilise plusieurs classes de réseau avec des règles d'isolement spécifiques :

| Classe | Domaine | Usage |
|--------|---------|-------|
| Surge | Secteur brut + transitoires | Broches PWR1, pastilles GDT, pastilles fusibles, Terre |
| HV | Secteur (après protection) | L1/L2/L3_VOLTAGE, NEUTRAL, PS1 côté AC |
| HV Divider | Points médians diviseurs | Réseau entre résistances HV et résistances de mesure |
| Power | 5 V / 3,3 V DC | +5 V, +3,3 V, GND, VCC |
| Low Power | Analogique / signal | VREF, AVCC, réseaux ampli-op |
| CT | Basse tension | Signaux transformateurs de courant |
| ANT | RF | Connecteur SMA vers module RFM69 (~8 mm de piste) |
| Gnd | Masse analogique | AGND |
| Default | Basse tension | Signaux généraux |

Les règles d'isolement HV sont définies dans `3phaseDiverter.kicad_dru`. L'isolement HV–LV est de 2,5 mm ; l'isolement HV–HV Divider est de 1,0 mm.

## Configuration

### Cavaliers de soudure

| Cavalier | Pôles | Fonction |
|----------|-------|----------|
| JP0 | 3 | Alimentation ATmega328P : 3,3 V (défaut) ou 5 V |
| JP1 | 3 | Broche A4 : mesure tension L3 (A4') ou I2C SDA |
| JP2 | 3 | Broche A5 : mesure courant L3 (A5') ou I2C SCL |
| JP3 | 2 | Configuration de déclenchement |
| JP4 | 3 | DS18B20 géré par le routeur (D3) ou par le module mk2Wifi (libellé « TEMP ») |
| GND_LINK | 2 | Pont entre GND et AGND (cavalier fil 0,75 mm²) |

### Monophasé vs triphasé

Tous les composants CMS sont assemblés en production, quelle que soit la configuration. La sélection monophasé/triphasé se fait par les cavaliers de soudure et le choix des connecteurs.

En **monophasé**, les cavaliers JP1 et JP2 sont configurés en position I2C (SDA/SCL), ce qui permet l'utilisation de l'écran OLED. Un connecteur PWR1 3 voies est fourni (Terre, Neutre, L1). Seul CT1 est raccordé.

En **triphasé**, les cavaliers JP1 et JP2 sont configurés pour les mesures L3 (position A4'/A5'), ce qui désactive l'afficheur OLED. Le connecteur PWR1 5 voies est utilisé et les trois CT sont raccordés.

## Intégration du module d'extension

La carte principale est conçue pour accueillir le module d'extension **mk2Wifi** via les connecteurs TRIG_EXT et UART_EXT :

- La carte principale utilise des **barrettes mâles** ; la mk2Wifi utilise des **barrettes femelles**
- L'alimentation +5 V est fournie par la carte principale via UART_EXT broche 3
- L'UART (TX/RX) assure la communication série avec le module d'extension
- Le signal DS18B20 est acheminé via UART_EXT broche 2 pour la mesure de température 1-Wire
- Les signaux GPIO D5–D9 fournissent les sorties de déclenchement/commande via TRIG_EXT
- Le bus I2C (SCL/SDA) est **local au module mk2Wifi uniquement** — il relie l'ESP32-C3 à l'écran OLED et n'est pas routé vers la carte principale

## Programmation

Le connecteur **FTDI** (Molex SL 1×6) permet le téléversement du firmware via un adaptateur USB-série FTDI ou compatible :

1. **Connexion** : brancher l'adaptateur FTDI sur le connecteur J0. Le brochage est compatible avec les câbles FTDI standard (GND sur la broche 1).
2. **Auto-reset** : le signal DTR déclenche un reset automatique de l'ATmega328P via un condensateur de couplage, permettant le téléversement sans intervention manuelle.
3. **Environnement** : compatible Arduino (ATmega328P avec bootloader). Utiliser la carte « Arduino Uno » ou équivalent dans l'IDE Arduino.

### Capteur de température DS18B20

Le capteur 1-Wire DS18B20 est toujours connecté sur la carte principale. Le cavalier **JP4** permet de choisir qui gère le capteur :
- **Position routeur** : le signal est acheminé vers la broche D3 de l'ATmega328P
- **Position mk2Wifi** : le signal est acheminé vers le module d'extension via UART_EXT broche 2

La résistance de pull-up nécessaire est intégrée sur la carte (R6, 4,7 kΩ).
