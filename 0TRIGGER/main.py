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
else:
    raise RuntimeError("BMP sensor not found")

bmp = BMP(i2c, addr = bmp_address)
print(">> BMP sensor initialisation successful at address {} ({})".format(bmp_address, hex(bmp_address)))


# ================================== LOOP ==================================
ps = 0
p0 = 0
N = 1000

for _ in range(N):
    p0 += bmp.read()["pressure"] / N

print(p0)

def altitude(pressure, temperature = 0):
    return 44330 * (1 - (pressure/p0) ** (1/5.255))

N2 = 10 # seems fine
ps = [bmp.read()["pressure"] for _ in range(N2)]
pss = [0] * 10

while True:
    pres_now = bmp.read()["pressure"]
    ps.pop(0)
    ps.append(pres_now)
    pressure = sum(ps)/N2
    pss.pop(0)
    pss.append(pressure)
    
    print(altitude(pressure), altitude(pres_now))
    utime.sleep(0.01)
    