Français | **[English](Readme.en.md)**

# mk2Wifi

Module d’extension WiFi/BLE pour la carte principale Mk2 PV Router.

## Présentation

La carte mk2Wifi ajoute une connectivité sans fil au Mk2 PV Router grâce à un module **ESP32-C3-MINI-1** (RISC-V simple cœur, WiFi 4, Bluetooth LE 5). Elle se branche directement sur la carte principale via les connecteurs TRIG_EXT et UART_EXT, et est alimentée en +5 V par la carte principale, régulé localement en +3,3 V.

Caractéristiques principales :
- WiFi 802.11 b/g/n (2,4 GHz) et Bluetooth LE 5
- Connecteur USB-C pour le chargement initial du firmware (mises à jour suivantes via OTA)
- Écran OLED optionnel via I2C (connecteur Molex SL)
- Cinq sorties GPIO de déclenchement/commande (D5–D9) vers la carte principale
- Passthrough du capteur de température 1-Wire DS18B20
- Liaison série UART avec la carte principale

## Images de la carte

| Face avant (assemblée) | Face arrière |
|:-:|:-:|
| ![Avant](assets/mk2Wifi-front.png) | ![Arrière](assets/mk2Wifi-back.png) |

| Composants CMS uniquement | Circuit imprimé nu |
|:-:|:-:|
| ![CMS](assets/mk2Wifi-smd.png) | ![Nu](assets/mk2Wifi-bare.png) |

## Schéma

[![Schéma mk2Wifi-C3](assets/mk2Wifi-C3-schematic.svg)](assets/mk2Wifi-C3-schematic.pdf)

## Fichiers de conception

| Fichier | Description |
|---------|-------------|
| `mk2Wifi.kicad_pro` | Fichier projet KiCad 9 |
| `mk2Wifi.kicad_sch` | Schéma |
| `mk2Wifi.kicad_pcb` | Circuit imprimé |
| `mk2Wifi.kicad_dru` | Règles de conception |
| `mk2Wifi.kicad_sym` | Bibliothèque de symboles locale |
| `sym-lib-table` | Table des bibliothèques de symboles |
| `fp-lib-table` | Table des bibliothèques d’empreintes |

## Nomenclature (BOM)

| Réf | Valeur | Boîtier | Description |
|-----|--------|---------|-------------|
| U1 | ESP32-C3-MINI-1 | ESP32-C3-MINI-1 | Module MCU avec WiFi/BLE |
| U2 | AP2112K-3.3 | SOT-23-5 | Régulateur LDO 3,3 V (600 mA) |
| TRIG_EXT | TRIG_EXT | PinSocket 1x06 2,54 mm | Connecteur déclenchement/GPIO |
| USB-C | USB_C_Receptacle | CSP-USC16-TR | Embase USB Type-C |
| UART_EXT | UART_EXT | PinSocket 1x06 2,54 mm | Connecteur UART + DS18B20 |
| OLED | OLED | Molex SL 1x04 2,54 mm | Connecteur écran OLED |
| D1 | LED | 0603 | Témoin d’alimentation |
| SW1 | SW_Push | CK PTS636S | Bouton boot/reset |
| R1 | 10K | 0402 | Pull-up EN |
| R2 | 1K | 0402 | Limitation de courant LED |
| R3 | 10K | 0402 | Pull-up GPIO8 (strapping) |
| R4 | 10K | 0402 | Pull-up GPIO2 (strapping) |
| R5 | 1K | 0402 | Protection série D9 (GPIO7) |
| R6 | 1K | 0402 | Protection série D6 (GPIO10) |
| R7 | 5K1 | 0402 | Pull-down USB CC1 |
| R8 | 5K1 | 0402 | Pull-down USB CC2 |
| R9 | 1K | 0402 | Protection série D7 (GPIO1) |
| R10 | 1K | 0402 | Protection série D5 (GPIO4) |
| R11 | 1K | 0402 | Protection série D8 (GPIO0) |
| C1 | 100nF | 0402 | Découplage +3,3 V |
| C2 | 4,7uF | 0603 | Condensateur sortie régulateur |
| C4 | 100nF | 0402 | Découplage +3,3 V (EN/OLED) |
| C5 | 4,7uF | 0603 | Condensateur entrée régulateur |

## Brochage des connecteurs

### TRIG_EXT (barrette 1x6)

| Broche | Signal |
|--------|--------|
| 1 | GND |
| 2 | D8 |
| 3 | D7 |
| 4 | D6 |
| 5 | D5 |
| 6 | D9 |

### UART_EXT (barrette 1x6)

| Broche | Signal |
|--------|--------|
| 1 | GND |
| 2 | DS18B20 |
| 3 | +5 V |
| 4 | UART_RX |
| 5 | UART_TX |
| 6 | NC |

Les noms des signaux (UART_TX, UART_RX) sont du point de vue de la **carte principale** : UART_TX transporte les données émises par la carte principale, reçues par l’ESP32-C3 sur GPIO20/U0RXD.

### OLED (Molex SL 1x4)

| Broche | Signal |
|--------|--------|
| 1 | GND |
| 2 | VCC (+3,3 V) |
| 3 | SCL |
| 4 | SDA |

## Affectation des GPIO de l’ESP32-C3

### GPIO connecteurs

| GPIO | Broche | Fonction | Notes |
|------|--------|----------|-------|
| GPIO0 | 12 | D8 (sortie déclenchement) | Résistance série 1K (R11) vers TRIG_EXT broche 2 |
| GPIO1 | 13 | D7 (sortie déclenchement) | Résistance série 1K (R9) vers TRIG_EXT broche 3 |
| GPIO3 | 6 | DS18B20 (1-Wire) | Direct vers UART_EXT broche 2 |
| GPIO4 | 18 | D5 (sortie déclenchement) | Résistance série 1K (R10) vers TRIG_EXT broche 5 |
| GPIO5 | 19 | SDA (données I2C) | Direct vers OLED broche 4 |
| GPIO6 | 20 | SCL (horloge I2C) | Direct vers OLED broche 3 |
| GPIO7 | 21 | D9 (sortie déclenchement) | Résistance série 1K (R5) vers TRIG_EXT broche 6 |
| GPIO10 | 16 | D6 (sortie déclenchement) | Résistance série 1K (R6) vers TRIG_EXT broche 4 |
| GPIO18 | 26 | USB D- | Vers USB-C |
| GPIO19 | 27 | USB D+ | Vers USB-C |
| GPIO20 | 30 | UART RX (U0RXD) | Reçoit le TX de la carte principale via UART_EXT broche 5 |
| GPIO21 | 31 | UART TX (U0TXD) | Émet vers le RX de la carte principale via UART_EXT broche 4 |

### GPIO internes

| GPIO | Broche | Fonction | Notes |
|------|--------|----------|-------|
| GPIO2 | 5 | Broche strapping | Pull-up 10K (R4) ; doit être haut au démarrage |
| GPIO8 | 22 | Broche strapping | Pull-up 10K (R3) ; doit être haut pour démarrage normal |
| GPIO9 | 23 | Bouton boot | SW1 tire vers GND ; maintenir bas au démarrage pour le mode téléchargement |

## Alimentation

En fonctionnement normal, le **+5 V** est fourni par la carte principale via le connecteur UART_EXT (broche 3). Le régulateur LDO AP2112K-3.3 (U2) convertit cette tension en +3,3 V pour l’ESP32-C3 et l’écran OLED, avec un courant maximal de 600 mA.

Découplage :
- C5 (4,7 µF) en entrée du régulateur (+5 V)
- C2 (4,7 µF) en sortie du régulateur (+3,3 V)
- C1, C4 (100 nF chacun) découplage local sur les rails +3,3 V

Le connecteur USB-C peut également fournir du +5 V lors de la programmation initiale, lorsque la carte n’est pas connectée à la carte principale. R7 et R8 (5K1 chacune) sur CC1/CC2 configurent le port USB-C en UFP (récepteur) pour demander 5 V à l’hôte.

> **ATTENTION :** Ne pas connecter l’USB-C lorsque la carte mk2Wifi est branchée sur la carte principale. Les deux alimentations +5 V (USB et carte principale) ne sont pas isolées et les connecter simultanément peut endommager la carte ou l’hôte USB.

D1 est une LED témoin d’alimentation, allumée en permanence lorsque le +3,3 V est présent (courant limité par R2).

## Intégration avec la carte principale

La carte mk2Wifi se branche sur les connecteurs **TRIG_EXT** et **UART_EXT** de la carte principale :

- La mk2Wifi utilise des **barrettes femelles** ; la carte principale utilise des **barrettes mâles**
- L’alimentation +5 V est fournie par la carte principale via UART_EXT broche 3
- L’UART (TX/RX) assure la communication série avec l’ATmega328P de la carte principale
- Le signal DS18B20 est acheminé pour la mesure de température 1-Wire
- Les signaux GPIO D5–D9 fournissent les sorties de déclenchement/commande
- Le bus I2C (SCL/SDA) est **local à la carte mk2Wifi uniquement** — il relie l’ESP32-C3 à l’écran OLED et n’est pas routé vers la carte principale

## Programmation

1. **Chargement initial du firmware :** Débrancher la carte de la carte principale, puis connecter un câble USB-C. L’ESP32-C3 dispose d’un contrôleur USB-série/JTAG intégré — aucun programmateur externe n’est nécessaire.
2. **Mode téléchargement :** Maintenir SW1 enfoncé (GPIO9 à l’état bas) pendant la mise sous tension, puis relâcher.
3. **Mises à jour suivantes :** Utiliser les mises à jour OTA (Over-The-Air) via WiFi. La connexion USB-C n’est nécessaire que pour le premier chargement.
