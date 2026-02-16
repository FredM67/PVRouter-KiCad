Français | **[English](Readme.en.md)**

# PVRouter-KiCad

Fichiers de conception KiCad pour le **Mk2 PV Router** — un système open-source de routage solaire photovoltaïque triphasé.

Inspiré par [www.mk2pvrouter.co.uk](https://www.mk2pvrouter.co.uk), ce projet fournit les schémas et circuits imprimés nécessaires pour construire un routeur PV capable de dévier l’excédent de production solaire vers des charges résistives (chauffe-eau, radiateurs, etc.).

![Carte principale](mainboard/3phaseDiverter.png)

## Structure du dépôt

| Répertoire | Description | État |
|------------|-------------|------|
| [`mainboard/`](mainboard/) | Carte principale universelle (3phaseDiverter) — rév. 4.1 | Conception active |
| [`output_stage/`](output_stage/) | Étage de puissance de sortie (carte séparée) | Conception active |
| [`expansion_boards/mk2Wifi/`](expansion_boards/mk2Wifi/) | Module d’extension WiFi/BLE (ESP32-C3) | Conception active |
| [`expansion_boards/ESP32/`](expansion_boards/ESP32/) | Module d’extension ESP32 | En développement |
| [`1-phase/`](1-phase/) | Variante monophasée (schéma uniquement, pas de PCB) | Archive |
| [`3-phase/`](3-phase/) | Variante triphasée (ancienne version) | Obsolète |
| [`KiCad/`](KiCad/) | Bibliothèques partagées (symboles, empreintes, modèles 3D) | — |

## Carte principale

La carte principale est le cœur du projet. Elle intègre :

- Microcontrôleur ATmega328P
- Trois capteurs de courant (transformateurs de courant)
- Trois capteurs de tension (ZMPT101B)
- Module radio RFM69 (433 MHz)
- Alimentation intégrée à partir du secteur
- Protection contre les surtensions (GDT + fusibles)
- Connecteurs d’extension (TRIG_EXT, UART_EXT)

La carte est conçue pour être montée dans un boîtier Schneider Electric Thalassa.

## Modules d’extension

- **[mk2Wifi](expansion_boards/mk2Wifi/)** — Module WiFi/BLE basé sur l’ESP32-C3-MINI-1, avec connecteur USB-C, écran OLED optionnel et capteur de température DS18B20
- **[ESP32](expansion_boards/ESP32/)** — Module d’extension ESP32

## Étage de puissance

L’**[étage de puissance](output_stage/)** est une carte séparée qui gère la commutation des charges résistives via des triacs ou des relais statiques (SSR).

## Outils requis

- [KiCad 9.0](https://www.kicad.org/) ou supérieur
- Les bibliothèques personnalisées sont incluses dans le répertoire `KiCad/` et référencées automatiquement via les fichiers `fp-lib-table` et `sym-lib-table`

## Liens

- Site de référence : [www.mk2pvrouter.co.uk](https://www.mk2pvrouter.co.uk)
- GitHub : [github.com/FredM67/PVRouter-KiCad](https://github.com/FredM67/PVRouter-KiCad)
