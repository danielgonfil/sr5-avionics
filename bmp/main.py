# import the required libraries
from bmp import *

from machine import Pin, I2C, SPI, UART
import utime

PIN_SCL = const(1)
PIN_SDA = const(0)

BMP_ADDRESS = const(119)

try:
    i2c = I2C(0, sda = Pin(PIN_SDA), scl = Pin(PIN_SCL), freq = 400000)
    print("I2C initialisation successful: {}".format(i2c))
except:
    raise RuntimeError

result = I2C.scan(i2c)
print("I2C scan result : ", result, [hex(i) for i in result]) # 118 in decimal is same as 0x76 in hexadecimal

if BMP_ADDRESS in result:
    bmp_address = BMP_ADDRESS

bmp = BMP(i2c, addr = bmp_address)
print(">> BMP sensor initialisation successful at address {} ({})".format(bmp_address, hex(bmp_address)))


# ================================== LOOP ==================================
ps = 0
p0 = 0
for _ in range(1000):
    p0 += bmp.read()["pressure"]

p0 = p0 / 1000

print(p0)

def altitude(pressure, temperature = 0):
    return 44330 * (1 - (pressure/p0) ** (1/5.255))

ps = 0

stored_values = []
n_stored_values = 100
leading_altitude = 0

APOGEE_DROP_THRESHOLD = 0.5 # meters

while True:
    stored_values.append(altitude(bmp.read()["pressure"]))
    if len(stored_values) == n_stored_values:
        stored_values.pop(0)
    
    current_altitude = sum(stored_values)/n_stored_values
    
    # detecting apogee: drop in altitude
    if current_altitude > leading_altitude:
        leading_altitude = current_altitude
    
    if leading_altitude - current_altitude > APOGEE_DROP_THRESHOLD:
        print("Apogee detected at altitude: ", leading_altitude)
        break

    print(leading_altitude, current_altitude)
    