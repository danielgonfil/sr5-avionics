import machine, utime

led = machine.Pin(25, machine.Pin.OUT)

print("Hello world")

for _ in range(6): # blink 3 times the led
    led.toggle()
    utime.sleep(1)