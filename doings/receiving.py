#receiver code:
from machine import UART, Pin
import time
uart = UART(1, 9600)                         # init with given baudrate
uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters

# uart = UART(1, 9600, rx=Pin(5), tx=Pin(4), bits=8, parity=None, stop=1, timeout=1)
print (uart)

b = None
msg = ""
while True:
    time.sleep(.1)
    if uart.any():
        # print(time.time())
        b = uart.read()
        # print(b)
        try:
            msg = b.decode('utf-8')
            # print(type(msg))
            print(msg)
        except Exception as e:
            print (e)