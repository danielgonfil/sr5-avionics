import machine
import utime

led = machine.Pin(25, machine.Pin.OUT)

print("Hello world")

for _ in range(10): # blink 10 times the led
    led.value(1)
    utime.sleep(1)
    led.value(0)
    utime.sleep(1)