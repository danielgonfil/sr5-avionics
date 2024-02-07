import machine
import time, utime
# import mpu6050_2

# Set up the I2C interface
i2c = machine.I2C(1,    sda=machine.Pin(14, pull=machine.Pin.PULL_UP), 
                        scl=machine.Pin(15, pull=machine.Pin.PULL_UP))

devices = i2c.scan()
device_count = len(devices)

if device_count == 0:
    print('No i2c device found.')
else:
    print(device_count, 'devices found.')

for device in devices:
    print('Decimal address:', device, ", Hex address: ", hex(device), "\t\t")
        
utime.sleep(1)