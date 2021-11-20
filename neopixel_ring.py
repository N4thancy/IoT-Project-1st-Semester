from machine import Pin
# import time
import neopixel

p = 15
n = 12

np = neopixel.NeoPixel(Pin(p), n)
goes = 0
rounds = 0
interval = 100
last_time = 0
max_rounds = 50

off = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

def set_green(i):
    np[i] = green

def set_red(i):
    np[i] = red

def set_off(i):
    np[i-3] = off

def led_full_stop():
    for i in range(n):
        np[i] = off

np[0] = off
np[1] = off
np[2] = off
np[3] = off
np[4] = off
np[5] = off
np[6] = off
np[7] = off
np[8] = off
np[9] = off
np[10] = off
np[11] = off
