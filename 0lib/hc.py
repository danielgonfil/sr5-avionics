from machine import Pin, UART
from CST import *
import utime

def raise_error(e):
   raise RuntimeError(e)

class Radio:
    def __init__(self):
        self.set_pin = Pin(HC_SET, Pin.OUT, value=1)
        self.hc = None
        try:
            self.hc = UART(1, 9600, rx=Pin(HC_RX), tx=Pin(HC_TX) , bits=8, parity=None, stop=1, timeout=1)
            utime.sleep(0.1)
            print("UART initialisation successful: {}".format(self.hc))
            print(">> HC initialisation successful")
        except Exception as error:
            raise_error("Problem with UART initialisation: " + str(error))
            
    def check_set_pin(self):
        self.set_pin.value(0)
        self.hc.write("AT")
        while not(self.hc.any()):
             utime.sleep(0.1)
        print(self.hc.read())
        self.set_pin.value(1)

    def set_power(self, power):
        if power not in list(range(0, 9)):
            print("This is not a valid power, setting MAX(8) by default")
            power = 8
        
        self.set_default()
        utime.sleep(0.1)
        
        self.set_pin.value(0)
        utime.sleep(0.1)
            
        try:
            self.hc.write("AT+P" + str(power))
        except Exception as error:
            print("Can't set power on radio: " + str(error))
        
        utime.sleep(0.1)
        while not(self.hc.any()):
            utime.sleep(0.1)
        
        print(self.hc.read())
        self.set_pin.value(1)
        utime.sleep(0.1)
    
    def receive_message(self):
        msg = ""
        try:
           msg = self.hc.read()
           msg.decode()
        except Exception as error:
           print("Cannot receive message: " + str(error))
        
        return msg
    
    def send_message(self, msg):
        try:
            self.hc.write(msg)
        except Except as error:
            print("Cannot send message: " + str(error))
    
    def set_baud_rate(self, baudrate):
        # hc.write("AT+B9600")
        if baudrate not in [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]:
            print("This is not a valid baudrate, setting 9600 by default")
            baudrate = 9600            
        
        self.set_default()
        utime.sleep(0.1)
        
        self.set_pin.value(0)
        utime.sleep(0.1)
        try:
            self.hc.write("AT+B" + str(baudrate))
        except Exception as error:
            print("Can't set baudrate on radio: " + str(error))
            
        utime.sleep(0.1)
        while not(self.hc.any()):
            utime.sleep(0.1)
        print(self.hc.read())
        self.set_pin.value(1)
        utime.sleep(0.1)
        
        
    def check_messages(self):
        return self.hc.any()
    
    
    def set_default(self):
        self.set_pin.value(0)
        utime.sleep(0.1)
        
        try:
            self.hc.write("AT+DEFAULT")
        except Exception as error:
            print("Can't set default: " + str(error))
            
        utime.sleep(0.1)
        
        while not(self.hc.any()):
            utime.sleep(0.1)
        
        print(self.hc.read())
        self.set_pin.value(1)
        utime.sleep(0.1)
    
    def get_BR(self):
        self.set_pin.value(0)
        utime.sleep(0.1)
        
        try:
            self.hc.write("AT+RB")
        except Exception as error:
            print("Can't set default: ")
            
        utime.sleep(0.1)
        
        while not(self.hc.any()):
            utime.sleep(0.1)
        
        print(self.hc.read())
        self.set_pin.value(1)
        utime.sleep(0.1)
        
    # set_default, time.sleep()

        
