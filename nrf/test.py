import machine, utime
from inter import*
from CST import*

# led = machine.Pin(PIN_GREEN_LED, machine.Pin.OUT)
led = LED(PIN_RED_LED)

led.on()

utime.sleep(1)

led.off()