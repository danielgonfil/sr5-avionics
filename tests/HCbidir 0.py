from machine import UART, Pin
import utime
# uart = UART(1, 9600)                         # init with given baudrate
# uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters

uart = UART(1, 9600, rx=Pin(5), tx=Pin(4), bits=8, parity=None, stop=1, timeout=1)
print (uart)

b = None
msg = "Hello there!"
flag = 0

while True:	
    if input("Send message:"):
        uart.write(msg)
        # print("Hello not there!")
        msg = 1
        
    else:
        b = uart.read()
        try:
            msg = b.decode('utf-8')
            print("Received message:", msg)
            utime.sleep(1)
        except Exception as e:
            print(e)
        msg = 0
        


