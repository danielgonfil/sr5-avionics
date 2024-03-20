from machine import Pin
from all import raise_error
import time

class LED(): # other pin connected to ground
    def __init__(self, pin):
        self.led = Pin(pin, Pin.OUT, value=1)
    
    def toggle(self):
        self.led.toggle()

    def blink(self, t, n):
        self.led.value(1) # off
        for _ in range(n):
            self.led.value(1) # on
            time.sleep(t)
            self.led.value(0) # off
            time.sleep(t)
    
    def on(self): self.led.value(1) # on
    def off(self): self.led.value(0) # off


class TEMP:
    def __init__(self):
        self.sensor = ADC(4)

    def read(self):
        adc_value = self.sensor.read_u16()
        volt = (3.3/65535) * adc_value
        temperature = 27 - (volt - 0.706)/0.001721
        return {"temp": temperature}

class Switch():
    def __init__(self):
        return
    
class Button():
    def __init__(self):
        return