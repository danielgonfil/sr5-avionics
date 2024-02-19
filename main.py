"""
all systems integrated together here
"""

from machine import Pin, I2C, SPI
import inter, mpu, bmp, sdcard, servo
import utime

# interfaces
led1 = inter.LED(25)

# sensors
MPU = mpu.MPU(I2C(0, scl = Pin(21), sda=Pin(20), freq=400000))
BMP = bmp.BMP(I2C(0, scl = Pin(1), sda = Pin(0),freq = 1000000), addr = 0x77, use_case = bmp.BMP280_CASE_WEATHER)

# data management
SD = sdcard.SDCard(SPI(1, baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=Pin(10), mosi=Pin(11), miso=Pin(8)),  Pin(9, Pin.OUT))

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
    print("Temperature: {:.2f} oC".format(data['temp']))

    utime.sleep(1)