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
    mpu = MPU(i2c, addr = mpu_address)
    print(">> MPU sensor initialisation successful at address {} ({})".format(mpu_address, hex(mpu_address)))
else:
    print("oops")

# ================================== LOOP ==================================
while True:
    data = mpu.read()

    # print(data["ax"], data["ay"], data["az"])
    print((data["ax"] ** 2 + data["ay"] ** 2 + data["az"] ** 2) ** .5)
    utime.sleep(.01)