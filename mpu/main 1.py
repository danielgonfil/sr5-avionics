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

ax = 0
ay = 0
az = 0

axs = [0]
ays = [0]
azs = [0]

N = 100

for _ in range(N):
    data = mpu.read()
    axs.append(data["ax"])
    ays.append(data["ay"])
    azs.append(data["az"])

from math import sqrt

ax = sum(axs) / N
ay = sum(ays) / N
az = sum(azs) / N

stdax = sqrt(sum((x - ax) ** 2 for x in axs) / N)
stday = sqrt(sum((x - ay) ** 2 for x in ays) / N)
stdaz = sqrt(sum((x - az) ** 2 for x in azs) / N)

std = sqrt(stdax ** 2 + stday ** 2 + stdaz ** 2) * 9.81

# Assuming functions to read accelerometer and initialize are defined as:
# initialize_accelerometer() and read_acceleration()
sampling_interval = 0.01  # 100 Hz sampling rate
previous_acceleration = [0, 0, 0]
previous_velocity = [0, 0, 0]  # This was missing and is necessary for the calculation
current_velocity = [0, 0, 0]
current_acceleration = [0, 0, 0]
position = [0, 0, 0]
baseline_acceleration = [ax, ay, az]  # Assuming this is defined somewhere after calibration
print(baseline_acceleration)

# Drift correction parameters
acceleration_threshold = [0.05, 0.05, 0.05]  # Threshold for zero-velocity condition, adjust based on noise level
velocity_threshold = [0.05, 0.05, 0.05]  # Minimum velocity to reset to zero, to avoid drift
vellist = []
acclist = []
heightlist = []

def add(l1: list, l2: list):
    return [a + b for a, b in zip(l1, l2)]

def sub(l1: list, l2: list):
    return [a - b for a, b in zip(l1, l2)]

def mul(l1: list, a: float):
    return [a * x for x in l1]

def read_acceleration():
    data = mpu.read()
    return [data["ax"], data["ay"], data["az"]]

def abss(list):
    return sum(x ** 2 for x in list) ** (0.5)

flag = 0
prev_time, time = utime.time_ns(), 0
print(stdax, stday, stdaz, std)

while True:
    time = utime.time_ns()
    dt = (time - prev_time) * 1e-9
    # print(time, prev_time, dt)
    prev_time = time

    current_acceleration = mul(sub(read_acceleration(), baseline_acceleration), 9.81)

    if abss(current_acceleration) < std:
        current_acceleration = [0, 0, 0]
        flag += 1
    else: flag = 0
    
    if flag >= 10:
        flag = 0
        current_velocity = [0, 0, 0]

    # current_velocity = add(current_velocity, mul(add(current_acceleration, previous_acceleration), 0.5 * sampling_interval))
    # print(current_acceleration, mul(current_acceleration, sampling_interval), add(current_velocity, mul(current_acceleration, sampling_interval)))
    current_velocity = add(current_velocity, mul(current_acceleration, dt))
    
    
        
    # position = add(position, mul(add(current_velocity, previous_velocity), 0.5 * sampling_interval))
    position = add(position, mul(current_velocity, dt))
    
    # previous_acceleration = current_acceleration
    # previous_velocity = current_velocity  # Update the previous velocity for next iteration
    
    utime.sleep(sampling_interval)
    print(["%.3f" % x if x < 0 else "+" + "%.3f" % x for x in current_acceleration], 
          ["%.3f" % x if x < 0 else "+" + "%.3f" % x for x in current_velocity] , 
          ["%.3f" % x if x < 0 else "+" + "%.3f" % x for x in position])