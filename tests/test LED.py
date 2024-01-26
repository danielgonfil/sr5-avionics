import machine, utime

led = machine.Pin(13, machine.Pin.OUT)

for _ in range(6):
    led.toggle()
    utime.sleep(1)
