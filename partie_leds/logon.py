from PIL import Image
import math
import time
import board
import adafruit_dotstar
    
dt =  0.01
# ==========================
# Capteur Hall 
# ==========================

# ==========================
# Configuration
# ==========================
NUM_LEDS = 72
sensor = 0  # passera à 1 quand la position de référence est atteinte
#ok
# East
strip_e = adafruit_dotstar.DotStar(board.D3, board.D2, NUM_LEDS, brightness=0.1, auto_write=False)
# North
strip_n = adafruit_dotstar.DotStar(board.D11, board.D10, NUM_LEDS, brightness=0.1, auto_write=False)
# West
strip_w = adafruit_dotstar.DotStar(board.D21, board.D20, NUM_LEDS, brightness=0.1, auto_write=False)
# South
strip_s = adafruit_dotstar.DotStar(board.D15, board.D14, NUM_LEDS, brightness=0.1, auto_write=False)

# ==========================
# Image
# ==========================
img = Image.open("logo.jpg").resize((144, 144)).convert("RGB")
width, height = img.size
center_x, center_y = width // 2, height // 2

# ==========================
# Polar -> pixel
# ==========================
def get_pixel_from_polar(angle_deg, radius):
    angle_rad = math.radians(angle_deg)
    x = int(center_x + radius * math.cos(angle_rad))
    y = int(center_y - radius * math.sin(angle_rad))  
    if 0 <= x < width and 0 <= y < height:
        return img.getpixel((x, y))
    return (0, 0, 0)

# ==========================
# Displays a strip
# ==========================
def display_strip(strip, angle_deg):
    for r in range(NUM_LEDS):
        strip[r] = get_pixel_from_polar(angle_deg, NUM_LEDS -1 - r)
    strip.show()

# = Main loop
# ==========================
global_angle = 0

while True:

    # --- Reference position : angle = 0 ---
    if sensor == 1:
        global_angle = 0
        sensor = 0  

    # --- Processing angles ---
    angle_e = (global_angle + 0) % 360
    angle_n = (global_angle + 90) % 360
    angle_w = (global_angle + 180) % 360
    angle_s = (global_angle + 270) % 360

    # --- Displaying in real time ---x
    display_strip(strip_e, angle_e)
    display_strip(strip_n, angle_n)
    display_strip(strip_w, angle_w)
    display_strip(strip_s, angle_s)

    # --- Rotation ---
    global_angle = (global_angle + 1) % 360
    time.sleep(dt)
