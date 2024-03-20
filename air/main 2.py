# import the required libraries
from bmp import *
from mpu import *
from sdcard import *
from picotemp import *
from inter import *

from machine import Pin, I2C, SPI, UART
import utime
from CST import *

state = STATE_IDLE

# ================================== FUNC ==================================
def raise_error_0(e):
   state = STATE_GND_ERROR
   raise RuntimeError(e)

def raise_error(e, green_led, yellow_led, red_led):
   state = STATE_GND_ERROR
   green_led.off()
   yellow_led.off()
   red_led.on()
   raise RuntimeError(e)

def LED_init(pin: int, i: int):
    try:
        led = LED(pin)
        if i == 1:
            led.on()
        else:
            led.off()
    except:
        raise_error_0("Problem with LED initialisation on pin {}".format(pin))
    
    return led

def INTER_init():
    print("="*60)
    try:
        green_led = LED_init(PIN_GREEN_LED, 0)
        yellow_led = LED_init(PIN_YELLOW_LED, 1)
        red_led = LED_init(PIN_RED_LED, 0)
    except:
        raise_error_0("Problem with LED initialisation")
    
    print(">> Interfaces initialisation successful")

    return green_led, yellow_led, red_led

def INIT_i2c(sda_pin, scl_pin):
    try:
        i2c = I2C(0, sda = Pin(sda_pin), scl = Pin(scl_pin), freq = 400000)
        print("I2C initialisation successful: {}".format(i2c))

        # scan
        scan = I2C.scan(i2c)
        print("I2C scan result : ", scan, [hex(i) for i in scan]) 

    except:
        raise_error("Problem with I2C initialisation")
    
    return i2c

def INIT_MPU(i2c):
    scan = I2C.scan(i2c)
    
    if scan == CORRECT_I2C:
        mpu_address = scan[1]
    elif MPU_ADDRESS in I2C.scan(i2c):
        mpu_address = MPU_ADDRESS
    else:
        raise_error("Problem with the i2c addresses (MPU)")
    
    try:
        mpu = MPU(i2c, addr = MPU_ADDRESS)
        print(">> MPU sensor initialisation successful at address {} ({})".format(mpu_address, hex(mpu_address)))
    except:
        raise_error("Problem with MPU sensor initialisation at address {} ({})".format(mpu_address, hex(mpu_address)))
    
    return mpu

def INIT_BMP(i2c):
    scan = I2C.scan(i2c)
    
    if scan == CORRECT_I2C:
        bmp_address = scan[2]
    elif BMP_ADDRESS in I2C.scan(i2c):
        bmp_address = BMP_ADDRESS
    else:
        raise_error("Problem with the i2c addresses (MPU)")
    
    try:
        mpu = MPU(i2c, addr = BMP_ADDRESS)
        print(">> BMP sensor initialisation successful at address {} ({})".format(bmp_address, hex(bmp_address)))
    except:
        raise_error("Problem with MPU sensor initialisation at address {} ({})".format(bmp_address, hex(bmp_address)))
    
    return mpu

def INIT_SD(cs_pin, sck_pin, mosi_pin, miso_pin):
    try:
        cs = Pin(cs_pin, Pin.OUT)
        print("CS initialisation successful: {}".format(cs))
    except:
        raise_error("Problem with CS initialisation")

    try:
        spi = SPI(1,
                    baudrate = 1000000,
                    polarity = 0,
                    phase = 0,
                    bits = 8,
                    firstbit = SPI.MSB,
                    sck = Pin(sck_pin),
                    mosi = Pin(mosi_pin),
                    miso = Pin(miso_pin))

        print("SPI initialisation successful: {}".format(spi))
    except:
        raise_error("Problem with SPI initialisation")
    
    try:
        SD = SDCard(spi, cs)
        print(">> SD card initialisation successful")
    except:
        raise_error("Problem with SD card initialisation")
    
    return SD

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

def MOUNT_SD(sd):
    file_count = 0
    vfs = os.VfsFat(sd)
    try:
        try:
            os.mount(sd, '/sd')
            dir = os.listdir('/sd')        
        except:
            os.mount(sd, '/')
            dir = os.listdir('/')
        
        file_count = get_file_count(dir)
        print("SD card filesystem mount successful: ", dir, ". File count: ", file_count)
        file_count += 1

    except:
        raise_error("Problem with SD card filesystem mount")
    
    return file_count + 1

def INIT_UART(rx_pin, tx_pin):
    try:
        uart = UART(1, 9600, rx=Pin(rx_pin), tx=Pin(tx_pin) , bits=8, parity=None, stop=1, timeout=1)
        print("UART initialisation successful: {}".format(hc))
        print(">> HC initialisation successful")
    except:
        raise_error("Problem with UART initialisation")
    
    return uart

def INIT_TEMP():
    try:
        temp = TEMP()
        print(">> Temp initialisation successful")
    except:
        raise_error("Problem with Temp initialisation")
    
    return temp

def INIT():
    print(">> Initialisaton starting...")
    start_time = utime.time_ns()
    state = STATE_INIT

    green_led, yellow_led, red_led = INTER_init()
    yellow_led.on()

    i2c = INIT_i2c(PIN_SDA, PIN_SCL)
    mpu = INIT_MPU(i2c)
    bmp = INIT_BMP(i2c)

    sd = INIT_SD(SD_CS, SD_SCK, SD_MOSI, SD_MISO)
    file_count = MOUNT_SD(sd)

    hc = INIT_UART(HC_RX, HC_TX)

    temp = INIT_TEMP()

    print(">> Initialisations successfully completed in", (utime.time_ns() - start_time) * 1e-9, "s")
    
    yellow_led.off()

    return green_led, yellow_led, red_led, mpu, bmp, sd, file_count, hc, temp

def read_data(mpu, bmp, temp):
    try:
        mpu_data = mpu.read()
        bmp_data = bmp.read()
        temp_data = temp.read()
    except:
        raise_error("Problem with data reading")

    return {"state": state,
            "time": utime.time_ns(),
            "mpu temp": mpu_data["temp"],
            "bmp temp": bmp_data["temp"],
            "pico temp": temp_data["temp"],
            "pres": bmp_data["pressure"],
            "ax" : mpu_data["ax"],
            "ay" : mpu_data["ay"],
            "az" : mpu_data["az"],
            "gx" : mpu_data["gx"],
            "gy" : mpu_data["gy"],
            "gz" : mpu_data["gz"]}

def data_str(data):
    return str(data["state"]) + ", " + str(data["time"]) + ", " + str(data["mpu temp"]) + ", " + str(data["bmp temp"]) + ", " + str(data["pico temp"]) + ", " + str(data["pres"]) + ", " + str(data["alt HYP"]) + ", " + str(data["alt IBF"]) + ", " + str(data["ax"]) + ", " + str(data["ay"]) + ", " + str(data["az"]) + ", " + str(data["gx"]) + ", " + str(data["gy"]) + ", " + str(data["gz"])

def save_data(data):
    # writting sd
    with open("/sd/{}.txt".format(file_count),"a+") as file:
        # file.write(str(state) + ", " + str(utime.time_ns()) + ", " + str(data["mpu temp"]) + ", " + str(data["bmp temp"]) + ", " + str(data["pico temp"]) + ", " + str(data["pres"]) + ", " + str(data["alt HYP"]) + ", " + str(data["alt IBF"]) + ", " + str(data["ax"]) + ", " + str(data["ay"]) + ", " + str(data["az"]) + ", " + str(data["gx"]) + ", " + str(data["gy"]) + ", " + str(data["gz"]))
        file.write(data_str(data) + "\n")
        file.close()

    # reading sd (for print)
    with open("/sd/{}.txt".format(file_count),"r") as file:
        if file != 0:
            print("Saved to \"{}.txt\": ".format(file_count), file.read())
            pass
        file.close()

def send_date(data):
    hc.write(data_str(data))

def CALLIBRATION(): return

# ================================== INIT ==================================
green_led, yellow_led, red_led, mpu, bmp, sd, file_count, hc, temp = INIT()
if state == STATE_INIT: # no problem during init -> callibration
    state = STATE_CALLIBRATION
    dt = DT_CALLIBRATION

# ================================== LOOP ==================================
while True:
    try:
        start_time = utime.time_ns()

        # ground
        if state == STATE_IDLE:
            dt = DT_IDLE
            state = STATE_INIT # UI (check button) / delay
            pass
        
        if state == STATE_INIT:
            dt = DT_INIT

            try:
                init_success, green_led, yellow_led, red_led, mpu, bmp, sd, file_count, hc, temp = INIT()
                
                if init_success: state = STATE_CALLIBRATION # no problem during init -> callibration
            
            except:
                state = STATE_GND_ERROR
            
            pass

        if state == STATE_CALLIBRATION:
            dt = DT_CALLIBRATION

            try:
                callibration_success = CALLIBRATION()
                if callibration_success: state = STATE_READY # no problem during callibration -> ready
            except:
                state = STATE_GND_ERROR
            
            pass 
        
        if state == STATE_GND_ERROR:
            dt = DT_GND_ERROR
            # wait for retry init 
            # UI -> IDLE
            pass
        
        if state == STATE_READY:
            dt = DT_READY
            pass
        
        # flight
        if state == STATE_ASCENT:
            dt = DT_ASCENT
            data = read_data()
            save_data(data)
            pass

        if state == STATE_DESCENT:
            dt = DT_DESCENT
            data = read_data()
            save_data(data)
            
            pass

        if state == STATE_LANDED:
            dt = DT_LANDED
            data = read_data()
            save_data(data)
            
            pass
        
        
        print("Loop done in {}".format((utime.time_ns() - start_time) * 1e-9))
        
        utime.sleep(dt)

    except:
        print("Loop problem")
        pass


# file: open once every 20 