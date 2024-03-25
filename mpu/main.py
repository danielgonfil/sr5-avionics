# import the required libraries
from mpu import *

from machine import Pin, I2C, SPI, UART
import utime

PIN_SCL = const(1)
PIN_SDA = const(0)

MPU_ADDRESS = const(104)

try:
    i2c = I2C(0, sda = Pin(PIN_SDA), scl = Pin(PIN_SCL), freq = 400000)
    print("I2C initialisation successful: {}".format(i2c))
except:
    raise RuntimeError

result = I2C.scan(i2c)
print("I2C scan result : ", result, [hex(i) for i in result]) # 118 in decimal is same as 0x76 in hexadecimal

if MPU_ADDRESS in result:
    mpu_address = MPU_ADDRESS
    mpu = MPU(i2c, address = mpu_address)
    print(">> MPU sensor initialisation successful at address {} ({})".format(mpu_address, hex(mpu_address)))
else:
    print("oops")

filter = []
for _ in range(100):
    filter.append(mpu.read()["az"])
    
a0 = 0
for _ in range(1000):
    filter.pop(0)
    filter.append(mpu.read()["az"])
    a0 += sum(filter) / len(filter) / 1000


filter = []
for _ in range(100):
    filter.append(mpu.read()["az"] - a0)

# ================================== LOOP ==================================
while True:
    data = mpu.read()["az"] - a0
    filter.pop(0)
    filter.append(data)
    print(sum(filter) / len(filter))
    utime.sleep(.01)