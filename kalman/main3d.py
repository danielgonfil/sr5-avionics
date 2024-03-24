# import the required libraries
from bmp import *
from mpu import *
from kalman3d import Kalman
from array import array

from machine import Pin, I2C
import utime

PIN_SCL = const(1)
PIN_SDA = const(0)

MPU_ADDRESS = const(104)
BMP_ADDRESS = const(119)


try:
    i2c = I2C(0, sda = Pin(PIN_SDA), scl = Pin(PIN_SCL), freq = 400000)
    print("I2C initialisation successful: {}".format(i2c))
except:
    raise RuntimeError

result = I2C.scan(i2c)
print("I2C scan result : ", result, [hex(i) for i in result]) # 118 in decimal is same as 0x76 in hexadecimal

if MPU_ADDRESS in result:
    try:
        mpu_address = MPU_ADDRESS
        mpu = MPU(i2c, addr = mpu_address)
        print(">> MPU sensor initialisation successful at address {} ({})".format(mpu_address, hex(mpu_address)))
    except:
        raise RuntimeError("Problem with MPU sensor initialisation")

if BMP_ADDRESS in result:
    try:
        bmp_address = BMP_ADDRESS
        bmp = BMP(i2c, addr = bmp_address)
        print(">> BMP sensor initialisation successful at address {} ({})".format(bmp_address, hex(bmp_address)))
    except:
        raise RuntimeError("Problem with BMP sensor initialisation at address")

# ================================== CALIB ==================================
def mean(list):
    return sum(list) / len(list)

def std(list):
    avg = mean(list)
    return (sum([(x - avg) ** 2 / len(list) for x in list])) ** 0.5

def altitude(pressure, p0):
    return 44330 * (1 - (pressure / p0) ** (1/5.255))

g = 9.81

p0 = 0
a0 = 0
ps = []
az = []
N = 100

for _ in range(N):
    p0 += bmp.read()["pressure"] / N
    a0 += mpu.read()["az"] * g / N

for _ in range(N):
    ps.append(bmp.read()["pressure"])
    az.append(mpu.read()["az"] * g)

pz = [altitude(p, p0) for p in ps]
f = 100
filter = Kalman(dt = 1 / f, std_acceletation = std(az), std_altitude = std(pz))

filter.S = array([[altitude(bmp.read()["pressure"], p0)],
                  [0], 
                  [mpu.read()["az"] * g - a0]])

# ================================== LOOP ==================================



while True:
    mpu_data = mpu.read()
    bmp_data = bmp.read()
    acceleration = mpu_data["az"] * g - a0
    height = altitude(bmp_data["pressure"], p0)
    filter.update(acceleration, height)
    print(filter.state[0][0], height, filter.state[1][0], filter.state[2][0], acceleration)
    utime.sleep(filter.dt)
