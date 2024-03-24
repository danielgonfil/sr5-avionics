from machine import Pin, I2C

PIN_SCL = const(1)
PIN_SDA = const(0)


i2c = I2C(0, sda = Pin(PIN_SDA), scl = Pin(PIN_SCL), freq = 400000)
print(i2c)

print(i2c.scan())
i2c.writeto_mem(0x68, 25, '\x70')
print(i2c.scan())
