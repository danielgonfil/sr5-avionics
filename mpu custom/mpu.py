from machine import Pin, I2C
import utime

PIN_SCL = const(1)
PIN_SDA = const(0)

PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
TEMP_OUT_H = 0x41
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

i2c = I2C(0, sda = Pin(PIN_SDA), scl = Pin(PIN_SCL), freq = 400000)
print(i2c)

i2c.writeto_mem(0x68, PWR_MGMT_1, b'\x00')
utime.sleep(0.100)
i2c.writeto_mem(0x68, SMPLRT_DIV, b'\x07')
i2c.writeto_mem(0x68, CONFIG, b'\x00')
i2c.writeto_mem(0x68, GYRO_CONFIG, b'\x00')
i2c.writeto_mem(0x68, ACCEL_CONFIG, b'\x00')

while True:
    high = i2c.readfrom_mem(0x68, 0x43, 1)[0]
    low = i2c.readfrom_mem(0x68, 0x44, 1)[0]
    print(high, low)
    # value = high << 8 | low
    # if value > 32768:
    #     value = value - 65536

    # print(value / 131.0)
