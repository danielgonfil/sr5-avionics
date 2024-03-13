from machine import UART, Pin
import utime
# uart = UART(1, 9600)                         # init with given baudrate
# uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters

uart = UART(1, 9600, rx=Pin(5), tx=Pin(4), bits=8, parity=None, stop=1, timeout=1)
print (uart)

b = None
msg = "Hello there!"
flag = 1

while True:	
    if flag == 0:
        uart.write("Hello there!")
        print("Hello there!")
        flag = 1
    else:
        if uart.any():
            b = uart.read()
            try:
                msg = b.decode('utf-8')
                print(msg)
                utime.sleep(1)
            except Exception as e:
                print(e)
            flag = 0
            


