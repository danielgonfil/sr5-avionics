#sender code:
from machine import UART, Pin, I2C
import utime, mpu

uart = UART(1, 9600, rx=Pin(5), tx=Pin(4) , bits=8, parity=None, stop=1, timeout=1)
print(uart)
i = 1

c = 3 * (10 ** 8)

sensor = machine.ADC(4)

def ReadTemperature():
 	adc_value = sensor.read_u16()
 	volt = (3.3/65535) * adc_value
 	temperature = 27 - (volt - 0.706)/0.001721
 	return round(temperature, 1)


i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)
MPU = mpu.MPU(i2c)

flag = 1 # 1 writin, 0 receiving

while True:
    # if flag == 0: # writing
    #     temperature = ReadTemperature()
        
    #     data = MPU.read()
    #     # print(str(data['temp']), str(temperature))
    #     msg = str(data['temp']) + " " + str(temperature) + "are you still receiving ???"
    #     uart.write(msg)

    #     flag = 1
     
    # if flag == 1: # receiving
    
    
    if uart.any():
        a = uart.read()
        try:
            time = int(a.decode('utf-8'))
            dt = utime.time()-time
            print(time, utime.time(), dt, dt*c)
        except Exception as e:
            print (e)
    
    utime.sleep(0.1)
    flag = 0
    