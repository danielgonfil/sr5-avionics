from machine import Pin, UART
import utime

HC_RX = const(5)
HC_TX = const(4)


uart = UART(1, 9600, rx = Pin(HC_RX), tx = Pin(HC_TX) , bits = 8, parity = None, stop = 1, txbuf = 256, rxbuf = 256, timeout = 1, timeout_char = 2)
#  uart = UART(1, 9600, rx = Pin(HC_RX), tx = Pin(HC_TX) , bits = 8, parity = None, stop = 1, timeout = 1)
print(uart)

# set_pin = Pin(0, mode = Pin.OUT, value = 0)
# set_pin.value(Pin.low)
# utime.sleep(0)

for _ in range(10):
    if uart.any():
        print(uart.read())
    utime.sleep(0.1)

while True:    
    utime.sleep(1)
    
    uart.write("AT+" + str(input("command:")))
    
    utime.sleep(1)

    while not(uart.any()):
        utime.sleep(0.1)

    print(uart.read())



# change FU + change P

