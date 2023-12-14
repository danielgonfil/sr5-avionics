"""
https://electrocredible.com/bmp280-raspberry-pi-pico-micropython-guide/
"""

from machine import Pin, I2C
from bmp280 import *
import time

sdaPIN = Pin(0)
sclPIN = Pin(1)
bus = I2C(0,sda=sdaPIN, scl=sclPIN, freq=400000)
bmp = BMP280(bus)

bmp.use_case(BMP280_CASE_INDOOR)

while True:
    pressure=bmp.pressure
    p_bar=pressure/100000
    p_mmHg=pressure/133.3224
    temperature=bmp.temperature
    print("Temperature: {} C".format(temperature))
    print("Pressure: {} Pa, {} bar, {} mmHg".format(pressure,p_bar,p_mmHg))
    time.sleep(1)