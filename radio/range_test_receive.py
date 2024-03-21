from machine import Pin, UART
import utime

HC_RX = const(5)
HC_TX = const(4)


uart = UART(1, 1200, rx = Pin(HC_RX), tx = Pin(HC_TX) , bits = 8, parity = None, stop = 1, txbuf = 256, rxbuf = 256, timeout = 1, timeout_char = 2)
#  uart = UART(1, 9600, rx = Pin(HC_RX), tx = Pin(HC_TX) , bits = 8, parity = None, stop = 1, timeout = 1)
print(uart)

led = Pin(20, mode = Pin.OUT, value = 0)
led.value(0)

while True:
    if uart.any():
        led.value(1)
        print("Received: ", uart.read())
        
        utime.sleep(0.2)
        led.value(0)
    
    else:
        utime.sleep(0.1)
