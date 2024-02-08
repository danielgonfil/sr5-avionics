from machine import Pin, I2C
from BMP import *
import time

sdaPIN = Pin(20)
sclPIN = Pin(21)
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