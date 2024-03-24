from machine import Pin, I2C
import time

PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
TEMP_OUT_H = 0x41
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

class MPU():
    def __init__(self, i2c, addr = 0x68):
        self.i2c = i2c

        self.i2c.writeto_mem(addr, PWR_MGMT_1, b'\x00')
        time.sleep_ms(100)
        self.i2c.writeto_mem(addr, SMPLRT_DIV, b'\x07')
        self.i2c.writeto_mem(addr, CONFIG, b'\x00')
        self.i2c.writeto_mem(addr, GYRO_CONFIG, b'\x00')
        self.i2c.writeto_mem(addr, ACCEL_CONFIG, b'\x00')
    
    def read_raw(self, addr, address = 0x68):
        high = self.i2c.readfrom_mem(address, addr, 1)[0]
        low = self.i2c.readfrom_mem(address, addr + 1, 1)[0]
        value = high << 8 | low
        if value > 32768:
            value = value - 65536
        return value
 
    def read(self):
        temp = self.read_raw(TEMP_OUT_H) / 340.0 + 36.53
        accel_x = self.read_raw(ACCEL_XOUT_H) / 16384.0
        accel_y = self.read_raw(ACCEL_XOUT_H + 2) / 16384.0
        accel_z = self.read_raw(ACCEL_XOUT_H + 4) / 16384.0
        gyro_x = self.read_raw(GYRO_XOUT_H) / 131.0
        gyro_y = self.read_raw(GYRO_XOUT_H + 2) / 131.0
        gyro_z = self.read_raw(GYRO_XOUT_H + 4) / 131.0
    
        return {"temp": temp, 
                "ax": accel_x, 
                "ay": accel_y, 
                "az": accel_z, 
                "gx": gyro_x, 
                "gy": gyro_y, 
                "gz": gyro_z}

def MPU_init(i2c, addr = 0x68):
    return MPU(i2c, addr)
