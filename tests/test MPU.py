from machine import Pin, I2C
import utime
from MPU import init_mpu6050, get_mpu6050_data

i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)
init_mpu6050(i2c)
 
while True:
    data = get_mpu6050_data(i2c)
    print("Temperature: {:.2f} oC".format(data['temp']))
    print("Acceleration: X: {:.2f}, Y: {:.2f}, Z: {:.2f} g"
          .format(data["ax"], data['ay'], data['az']))
    print("Gyroscope: X: {:.2f}, Y: {:.2f}, Z: {:.2f} o/s"
          .format(data['gx'],data['gy'], data['gz']))
    utime.sleep(1)