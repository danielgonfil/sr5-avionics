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
   raise RuntimeError(e)

# ================= temp =================
try:
    temp = TEMP()
    print(">> Temp initialisation successful")
except:
    raise_error("Problem with Temp initialisation")

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


import json

label_list = []
data_list = []

        
def create_json(dali,lali):
    print("Recording over.")
    chart_data = {
      "backgroundColor": "white",
      "width": 800,
      "height": 300,
      "format": "png",
        "chart":{
            "type":"line",
            "data":{
                "labels":lali,
                "datasets":[{"label":'Data',"data":dali,"fill":"false","borderColor":"blue",
                             "borderWidth":"1","pointRadius":1.3,"pointBorderColor":"green"}]
                }
            }
        
        }
    
    with open("adc_data.json", "w+") as datafile:
        json.dump(chart_data, datafile)
        print("JSON file created.")
        
for _ in range(100):
    pressure = mpu.read()["gz"]
    print(pressure)
    data_list.append(pressure)
    label_list.append(utime.time_ns())
    time.sleep(0.1)

create_json(data_list, label_list)
