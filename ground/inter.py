from machine import Pin
import time

class LED(): # other pin connected to ground
    def __init__(self, pin):
        self.led = Pin(pin, mode = Pin.OUT, value = 1)
    
    def toggle(self):
        self.led.toggle()

    def blink(self, t, n):
        self.led.value(0) # off
        for _ in range(n):
            self.led.value(1) # on
            time.sleep(t)
            self.led.value(0) # on
            time.sleep(t)
    
    def on(self): self.led.value(0)
    def off(self): self.led.value(1)


class Switch():
    def __init__(self):
        return
    
class Button():
    def __init__(self):
        return