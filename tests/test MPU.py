from machine import Pin, I2C
import utime
import mpu

i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)
mpu = mpu.MPU(i2c)
 
while True:
    data = mpu.read()
    print("Temperature: {:.2f} oC".format(data['temp']))
    print("Acceleration: X: {:.2f}, Y: {:.2f}, Z: {:.2f} g"
          .format(data["ax"], data['ay'], data['az']))
    print("Gyroscope: X: {:.2f}, Y: {:.2f}, Z: {:.2f} o/s"
          .format(data['gx'],data['gy'], data['gz']))
    utime.sleep(1)