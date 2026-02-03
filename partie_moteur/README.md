# PARTIE MOTEUR

## Contrôle moteur et mesure de vitesse par capteur Hall (Raspberry Pi)

Ce projet permet de :
- piloter un moteur via PWM (50 Hz)
- mesurer la vitesse de rotation avec un capteur à effet Hall
- générer une impulsion matérielle '1 tour' sur un GPIO
- superviser le système via une interface web

L’architecture sépare le temps réel GPIO (pigpiod) de la logique et de l’IHM (Python / Flask).

---

## Architecture

- pigpiod : gestion temps réel des GPIO (PWM, interruptions, impulsions précises)
- Python : logique de contrôle et agrégation des données
- Flask : serveur web
- HTML / JavaScript : interface de supervision
---

## Matériel requis

- Raspberry Pi (Raspberry Pi OS / Linux)
- Capteur Hall
- Moteur commandé par PWM (ESC)

### Connexions GPIO

- GPIO 18 : PWM moteur
- GPIO 17 : entrée capteur Hall
- GPIO 27 : impulsion '1 tour'

---

## Installation

### Installer pigpio

```bash
sudo apt update
sudo apt install pigpio python3-pigpio
sudo pigpiod
