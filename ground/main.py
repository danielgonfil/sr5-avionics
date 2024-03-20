# https://github.com/dafvid/micropython-bmp280
# import the required libraries
from machine import Pin, UART
import utime
from CST import *

start_time = utime.time_ns()
# ================================== INITIALISATOIN ==================================
# ================= radio ================= 
try:
    # hc = UART(1, 9600, rx=Pin(HC_RX), tx=Pin(HC_TX) , bits=8, parity=None, stop=1, timeout=1)
    uart = UART(1, 9600)
    uart.init(9600, bits=8, parity=None, stop=1)
    print("UART initialisation successful: {}".format(uart))
    print("HC initialisation successful")
except:
    raise RuntimeError("Problem with UART initialisation")

print("="*60)
print("="*60)
print(">> Initialisations successfully completed in", (utime.time_ns() - start_time) * 1e-9, "s")
print("="*60)
print("="*60)

# ================================== LOOP ==================================
while True:
    if uart.any():
        msg = uart.read()
        try:
            print(msg)
            data = msg.decode('utf-8').split(", ")
            data_dic = {"state": int(data[0]),
                    "time": int(data[1]),
                    "mpu temp": float(data[2]),
                    "bmp temp": float(data[3]),
                    "pico temp": float(data[4]),
                    "pres": float(data[5]),
                    "alt HYP": float(data[6]),
                    "alt IBF": float(data[7]),
                    "ax" : float(data[8]),
                    "ay" : float(data[9]),
                    "az" : float(data[10]),
                    "gx" : float(data[11]),
                    "gy" : float(data[12]),
                    "gz" : float(data[13])}
            print("\n"*2)
            
            print("state:", data[0])
            print("time:", data[1])
            print("mpu temp:", data[2])
            print("bmp temp:", data[3])
            print("pico temp:", data[4])
            print("pres:", data[5])
            print("alt HYP:", data[6])
            print("alt IBF:", data[7])
            print("ax:", data[8])
            print("ay:", data[9])
            print("az:", data[10])
            print("gx:", data[11])
            print("gy:", data[12])
            print("gz:", data[13])
            

        except Exception as e:
            print (e)
    
    utime.sleep(0)