""" 
https://how2electronics.com/interfacing-mpu6050-with-raspberry-pi-pico-micropython/
"""

from machine import Pin, I2C
import utime
from  mpu6050 import init_mpu6050, get_mpu6050_data, calculate_tilt_angles, complementary_filter
 
i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)
# init_mpu6050(i2c)
 
pitch = 0
roll = 0
# prev_time = utime.ticks_ms()

# while True:
#     data = get_mpu6050_data(i2c)
#     curr_time = utime.ticks_ms()
#     dt = (curr_time - prev_time) / 1000
 
#     tilt_x, tilt_y, tilt_z = calculate_tilt_angles(data['accel'])
#     pitch, roll = complementary_filter(pitch, roll, data['gyro'], dt)
 
#     prev_time = curr_time
 
#     print("Temperature: {:.2f} °C".format(data['temp']))
#     print("Tilt angles: X: {:.2f}, Y: {:.2f}, Z: {:.2f} degrees".format(tilt_x, tilt_y, tilt_z))
#     print("Pitch: {:.2f}, Roll: {:.2f} degrees".format(pitch, roll))
#     print("Acceleration: X: {:.2f}, Y: {:.2f}, Z: {:.2f} g".format(data['accel']['x'], data['accel']['y'], data['accel']['z']))
#     print("Gyroscope: X: {:.2f}, Y: {:.2f}, Z: {:.2f} °/s".format(data['gyro']['x'], data['gyro']['y'], data['gyro']['z']))
#     utime.sleep(1)