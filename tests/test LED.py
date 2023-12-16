from machine import Pin
import utime
led = Pin(13, Pin.OUT)
timer = Timer()

def blink():
    led.toggle()

while True:
    blink()
    utime.sleep(1000)
