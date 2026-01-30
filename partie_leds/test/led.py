import time
import board
import adafruit_dotstar
# Ceci est un code de test qui allume les 4 bandeaux de leds en les faisant clignonter de plus en plus vite
NUM_LEDS = 72 
#SPi 0
CLK_PIN0 = board.D11
DATA_PIN0 = board.D10

#SPI 6
CLK_PIN6 = board.D21
DATA_PIN6 = board.D20

#SPI 5
CLK_PIN5 = board.D15    
DATA_PIN5 = board.D14

#SPI 3
CLK_PIN3 = board.D3
DATA_PIN3 = board.D2


strip = adafruit_dotstar.DotStar(
    CLK_PIN0,
    DATA_PIN0,
    NUM_LEDS,
    brightness=0.2,
    auto_write=False
)
strip6 = adafruit_dotstar.DotStar(
    CLK_PIN6,
    DATA_PIN6,
    NUM_LEDS,
    brightness=0.2,
    auto_write=False
)
strip5 = adafruit_dotstar.DotStar(
    CLK_PIN5,
    DATA_PIN5,
    NUM_LEDS,
    brightness=0.2,
    auto_write=False
)
strip3 = adafruit_dotstar.DotStar(
    CLK_PIN3,
    DATA_PIN3,
    NUM_LEDS,
    brightness=0.2,
    auto_write=False
)
# Couleurs
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
OFF = (0, 0, 0)

# Préparer les buffers ON et OFF pour plus de vitesse
on_buffer = [None] * NUM_LEDS
off_buffer = [OFF] * NUM_LEDS

# Une LED sur deux : rouge / jaune
for i in range(NUM_LEDS):
    if i % 2 == 0:
        on_buffer[i] = RED
    else:
        on_buffer[i] = YELLOW

# Fréquences
FREQ_START = 1.0
FREQ_END = 3000
STEP = 5

current_freq = FREQ_START

while True:
    print(f"Fréquence : {current_freq:.2f} Hz")

    # Allume le motif rouge/jaune
    strip[:] = on_buffer
    strip6[:] = on_buffer
    strip5[:] = on_buffer
    strip3[:] = on_buffer

    strip.show()
    strip6.show()
    strip5.show()
    strip3.show()

    time.sleep(1 / (2 * current_freq))

    # Éteint toutes les LEDs
    strip[:] = off_buffer
    strip6[:] = off_buffer
    strip5[:] = off_buffer
    strip3[:] = off_buffer

    strip.show()
    strip6.show()
    strip5.show()
    strip3.show()

    time.sleep(1 / (2 * current_freq))

    # augmente la fréquence
    if current_freq < FREQ_END:
        current_freq += STEP
