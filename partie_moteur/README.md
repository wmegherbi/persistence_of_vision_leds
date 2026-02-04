# PARTIE MOTEUR



## Contrôle moteur et mesure de vitesse par capteur Hall (Raspberry Pi)

Ce projet permet de :
- piloter un moteur via PWM (50 Hz)
- mesurer la vitesse de rotation avec un capteur à effet Hall
- générer une impulsion matérielle '1 tour' sur un GPIO
- superviser le système via une interface web

![Uploading image.png…]()

---
## Table des matières

1. [Architecture](#architecture)
2. [Matériel requis](#matériel-requis)
   - [Connexions GPIO](#connexions-gpio)
3. [Installation](#installation)
   - [Installer pigpio](#installer-pigpio)
   - [Installer les dépendances Python](#2-installer-les-dependances-python)
4. [Utilisation](#utilisation)
   - [Lancer le programme](#lancer-le-programme)
   - [Accéder à l'interface web](#acceder-a-linterface-web)
5. [Fonctionnalités détaillées](#fonctionnalités)
6. [Fonctionnement interne](#fonctionnement-interne-résumé)
7. [Remarques](#remarques)


## Architecture

- pigpiod : gestion temps réel des GPIO (PWM)
- Python :  contrôle et géstion des données
- Flask : serveur web
- HTML / JavaScript : interface web

```` bash
partie_moteur/
├── web3_control.py    # Cœur du système : contrôle moteur, gestion capteur Hall, API Flask
├── requirements.txt    # Dépendances Python (flask, pigpio)
├── static/
│   ├── app.js          # Logique front-end (graphiques, interactions)
│   └── style.css       # Styles de l'interface utilisateur
└── templates/
    └── index.html      # Template HTML principal (interface de contrôle)
````
---

## Matériel requis

### Composants principaux
- **Raspberry Pi** avec **Raspberry Pi OS** 
- **Capteur à effet Hall** (ex: US5881, A3144 ou DRV5055) pour la détection des tours
- **Moteur brushless A2212 930KV** + **ESC 30A** (compatible PWM 50Hz)
- **Aimants**  à fixer sur roue pour déclencher le capteur Hall

### Connexions GPIO

| GPIO Raspberry Pi | Fonction                     | Détails                                                                 |
|-------------------|-------------------------------|-------------------------------------------------------------------------|
| GPIO 18           | Sortie PWM (commande moteur)  | Connecté à l'entrée PWM de l'ESC ou du contrôleur de moteur          |
| GPIO 17           | Entrée capteur Hall           | Configuré pour détecter les fronts montants/descendants                |
| GPIO 27           | Sortie impulsion "1 tour"     | Génère une impulsion de 100 µs à chaque tour complet du moteur         |

---

## Installation

### Installer pigpio

```bash
sudo apt update
sudo apt install pigpio python3-pigpio
sudo pigpiod
```

### 2) Installer les dependances Python

```bash
pip3 install flask pigpio
```

## Utilisation

### Lancer le programme :

```bash
python3 web3_control.py
````

### Accéder à l'interface web :

```bash
http://<IP_DU_RASPBERRY>:5000
````



## Fonctionnalités

- Slider PWM (1000–2000 µs)
- Bouton STOP

Affichage :
- nombre d'impulsions Hall
- nombre d'aimants par tour
- vitesse en tr/min
- visualisation PWM et impulsions '1 tour'

## Fonctionnement interne (résumé)

- Les fronts du capteur Hall sont traités par un callback pigpio
- Les données partagées sont protégées par un lock (thread safety)
- La vitesse est calculée via une fenêtre glissante de timestamps de 5 secondes
- Une impulsion courte (100 µs) est générée sur GPIO27 à chaque tour complet (quand 4 fronts sont déctetés du capteur effet hall)

### Flux de Données
1. **Capteur Hall → Raspberry Pi** :
   - Détection des fronts via `pigpio.callback()` (dans `web3_control.py`)
   - Stockage des timestamps dans `edge_times[]`

2. **Raspberry Pi → Interface Web** :
   - Données exposées via les endpoints Flask :
     - `/api/hall` (compteur, RPM)
     - `/api/pulse` (timestamps des impulsions)
   - Mise à jour en temps réel via JavaScript (`static/app.js`)

3. **Interface Web → Moteur** :
   - Contrôle PWM via le slider (POST sur `/set_live`)
   - Arrêt d'urgence (POST sur `/stop`)


## Remarques

- pigpiod doit être lancé avant le script
``` bash
sudo pigpiod
```



