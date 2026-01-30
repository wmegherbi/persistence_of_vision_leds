# Dans ce dossier, vous trouverez tout ce qu'il faut savoir pour faire fonctionner les LEDs sur le système
## Partie 1 : Connexion avec la Raspberry Pi
La Raspberry Pi est alimentée via le 5V qui sort du slip ring, relié à la prise secteur. C'est cette même alimentation qui alimente les LEDs via des connecteurs aux quatre coins de la roue. Pour lancer le programme sur la Raspberry Pi, on se connecte en SSH via un PC connecté au même réseau. Pour la première connexion, nous vous conseillons d'utiliser l'interface graphique de la rasp et de configurer vos paramètres réseau (nom du réseau et mot de passe) via un clavier, une souris et un écran connecté en HDMI à la carte. Notez également l'adresse IP de la rasp lorsqu'elle est connectée au réseau afin de configurer la liaison SSH.
### Le nom d'utilisateur et le mot de passe de cette Rasp sont respectivement se, se (nom d'utilisateur se, mot de passe se).
Une fois connecté en SSH, on se place dans le repértoire de travail et activons l'environnement virtuel Python dans lequel sont installées les bibliothèques nécessaires :
```bash
cd pr/
source venv/bin/activate
```
Notez qu'à chaque reboot de la carte, l'environnement venv doit être réactivé.
Il ne reste plus qu'à lancer le programme de votre choix :
```bash
python3 logon.py
```
## Partie 2 : Gestion des LEDs
### 1. Interfaces SPI
On a besoin de 4 interfaces SPI indépendantes et elles doivent être présentes dans /dev afin d'être détectées par la bibliothèques dotstar. Pour ce faire, voir Partie 3.
![brachements des LEDs sur la Raspberry Pi](images/schema_cablage.png)
