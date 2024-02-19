"""
all systems integrated together here
"""

from machine import Pin, I2C, SPI
import inter, mpu, sdcard, servo
import utime

# interfaces
led1 = inter.LED(25)

# sensors
MPU = mpu.MPU(I2C(0, scl=Pin(21), sda=Pin(20), freq=400000))

# data management
SD = sdcard.SDCard(SPI(1,
                    baudrate=1000000,
                    polarity=0,
                    phase=0,
                    bits=8,
                    firstbit=SPI.MSB,
                    sck=Pin(10),
                    mosi=Pin(11),
                    miso=Pin(8)), 
                  Pin(9, Pin.OUT))

# state:
#   state  |  id
#   idle   |   0
#   calib  |   1
#    run   |   2
#   error  |   3

STATE = 0

while True:
    led1.blink(0.1, 1)

    data = MPU.read()
#     print("Temperature: {:.2f} oC".format(data['temp']))
#     print("Acceleration: X: {:.2f}, Y: {:.2f}, Z: {:.2f} g"
#           .format(data["ax"], data['ay'], data['az']))
#     print("Gyroscope: X: {:.2f}, Y: {:.2f}, Z: {:.2f} o/s"
#           .format(data['gx'],data['gy'], data['gz']))
    utime.sleep(1)