import machine
import sdcard
import os

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(9, machine.Pin.OUT)

# Intialize SPI peripheral (start with 1 MHz)
spi = machine.SPI(1,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(10),
                  mosi=machine.Pin(11),
                  miso=machine.Pin(8))

# Initialize SD card
SD = sdcard.SDCard(spi, cs)

# Mount filesystem
vfs = os.VfsFat(SD)
try:
    os.mount(SD, '/sd')
    print(os.listdir('/sd'))
except:
    os.mount(SD, '/')
    print(os.listdir('/'))


# writting file
file = open("/sd/sample.txt","w")
for i in range(20):
    file.write("Sample text = %s\r\n" % i)
file.close()

# reading file
file = open("/sd/sample.txt", "r")
if file != 0:
    print("Reading from SD card")
    read_data = file.read()
    print (read_data)
file.close()