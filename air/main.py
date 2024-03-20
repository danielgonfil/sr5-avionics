# import the required libraries
from bmp import *
from mpu import *
from sdcard import *
from picotemp import *
from inter import *

from machine import Pin, I2C, SPI, UART
import utime
from CST import *


def raise_error(e):
   state = STATE_GND_ERROR
   green_led.off()
   yellow_led.off()
   red_led.on()
   raise RuntimeError(e)

state = STATE_IDLE
start_time = utime.time_ns()
# ================================== INITIALISATOIN ==================================
# ================= interface  ================= 
# leds
try:
    green_led = LED(PIN_GREEN_LED)
    green_led.off()
except:
    raise_error("Problem with green LED initialisation")
   
try:
    yellow_led = LED(PIN_YELLOW_LED)
    yellow_led.on()
except:
    raise_error("Problem with yellow LED initialisation")

try: 
    red_led = LED(PIN_RED_LED)
    red_led.off()
except:
    raise_error("Problem with red LED initialisation")

# button


print("Interfaces initialisation successful")
print("="*60)

# ================= sensors ================= 
# check i2c connections
try:
    i2c = I2C(0, sda = Pin(PIN_SDA), scl = Pin(PIN_SCL), freq = 400000)
    print("I2C initialisation successful: {}".format(i2c))
except:
    raise_error("Problem with I2C initialisation")


result = I2C.scan(i2c)
print("I2C scan result : ", result, [hex(i) for i in result]) # 118 in decimal is same as 0x76 in hexadecimal

if result == CORRECT_I2C:
    addresses = [hex(i) for i in result]
    print("Correct i2c addresses: ", addresses)
    mpu_address = result[1]
    bmp_address = result[2]

elif (MPU_ADDRESS in result) and (BMP_ADDRESS in result):
    addresses = [hex(i) for i in result]
    print("Problem with the i2c addresses: ", addresses, " Initialiazing...")
    mpu_address = MPU_ADDRESS
    bmp_address = BMP_ADDRESS

else:
    raise_error("Problem with the i2c addresses")

# init mpu sensor
try:
    mpu = MPU(i2c, addr = mpu_address)
    print(">> MPU sensor initialisation successful at address {} ({})".format(mpu_address, hex(mpu_address)))
except:
    raise_error("Problem with MPU sensor initialisation at address {} ({})".format(mpu_address, hex(mpu_address)))

# init bmp sensor
try:
    bmp = BMP(i2c, addr = bmp_address)
    print(">> BMP sensor initialisation successful at address {} ({})".format(bmp_address, hex(bmp_address)))
except:
    raise_error("Problem with BMP sensor initialisation at address {} ({})".format(bmp_address, hex(bmp_address)))


print("="*60)
# ================= init sd card ================= 
# Assign chip select (CS) pin (and start it high)
try:
    cs = Pin(SD_CS, Pin.OUT)
    print("CS initialisation successful: {}".format(cs))
except:
    raise_error("Problem with CS initialisation")

# Intialize SPI peripheral (start with 1 MHz)
try:
    spi = SPI(1,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=SPI.MSB,
                  sck=Pin(SD_SCK),
                  mosi=Pin(SD_MOSI),
                  miso=Pin(SD_MISO))

    print("SPI initialisation successful: {}".format(spi))
except:
    raise_error("Problem with SPI initialisation")
# Initialize SD card
try:
    SD = SDCard(spi, cs)
    print(">> SD card initialisation successful")
except:
    raise_error("Problem with SD card initialisation")

def get_file_count(dir):
    file_count = 0
    for file_name in dir:
        if ".txt" in file_name:
            file_name = file_name[:-4]
            try:
                n = int(file_name)
                if n > file_count:
                    file_count = n
            except:
                pass
    return file_count

# Mount filesystem
file_count = 0
vfs = os.VfsFat(SD)
try:
    try:
        os.mount(SD, '/sd')
        dir = os.listdir('/sd')        
    except:
        os.mount(SD, '/')
        dir = os.listdir('/')
    
    file_count = get_file_count(dir)
    print("SD card filesystem mount successful: ", dir, ". File count: ", file_count)
    file_count += 1

except:
    raise_error("Problem with SD card filesystem mount")

print("="*60)
# ================= radio ================= 
try:
    hc = UART(1, 9600, rx=Pin(HC_RX), tx=Pin(HC_TX) , bits=8, parity=None, stop=1, timeout=1)
    print("UART initialisation successful: {}".format(hc))
    print(">> HC initialisation successful")
except:
    raise_error("Problem with UART initialisation")

print("="*60)
# ================= temp =================
try:
    temp = TEMP()
    print(">> Temp initialisation successful")
except:
    raise_error("Problem with Temp initialisation")

print("="*60)
print("="*60)
print(">> Initialisations successfully completed in", (utime.time_ns() - start_time) * 1e-9, "s")
print("="*60)
print("="*60)

if state == STATE_IDLE: # no problem during idle -> callibration
    state = STATE_READY
    yellow_led.off()

import struct

# ================================== LOOP ==================================
while True:
    try:
        start_time = utime.time_ns()
        # reading data
        mpu_data = mpu.read()
        bmp_data = bmp.read()
        temp_data = temp.read()
        data = {"mpu temp": mpu_data["temp"],
                "bmp temp": bmp_data["temp"],
                "pico temp": temp_data["temp"],
                "pres": bmp_data["pressure"],
                "alt HYP": bmp_data["altitude HYP"],
                "alt IBF": bmp_data["altitude IBF"],
                "ax" : mpu_data["ax"],
                "ay" : mpu_data["ay"],
                "az" : mpu_data["az"],
                "gx" : mpu_data["gx"],
                "gy" : mpu_data["gy"],
                "gz" : mpu_data["gz"]}
        
        data_str = str(state) + ", " + str(utime.time_ns()) + ", " + str(data["mpu temp"]) + ", " + str(data["bmp temp"]) + ", " + str(data["pico temp"]) + ", " + str(data["pres"]) + ", " + str(data["alt HYP"]) + ", " + str(data["alt IBF"]) + ", " + str(data["ax"]) + ", " + str(data["ay"]) + ", " + str(data["az"]) + ", " + str(data["gx"]) + ", " + str(data["gy"]) + ", " + str(data["gz"])
        
        # writting sd
        with open("/sd/{}.txt".format(file_count),"a+") as file:
            # file.write(str(state) + ", " +
            #           str(utime.time_ns()) + ", " +
            #           str(data["mpu temp"]) + ", " +
            #           str(data["bmp temp"]) + ", " +
            #           str(data["pico temp"]) + ", " +
            #           str(data["pres"]) + ", " +
            #           str(data["alt HYP"]) + ", " +
            #           str(data["alt IBF"]) + ", " +
            #           str(data["ax"]) + ", " +
            #           str(data["ay"]) + ", " +
            #           str(data["az"]) + ", " +
            #           str(data["gx"]) + ", " +
            #           str(data["gy"]) + ", " +
            #           str(data["gz"]))
            file.write(data_str + "\n")
            file.close()

        # reading sd (for print)
        with open("/sd/{}.txt".format(file_count),"r") as file:
            if file != 0:
                print("Saved to \"{}.txt\": ".format(file_count), file.read())
                pass
            file.close()
        
        #transmit over radio
        hc.write(data_str)
        hc.write(str(utime.time()))
        print("Loop time: ", (utime.time_ns() - start_time) * 1e-9, "s")
        green_led.blink(0.5, 1)
    
    except:
        raise_error("Loop problem")
