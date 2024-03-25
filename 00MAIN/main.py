from lib.fsmachine import *
from lib.events import *
import utime

# ==============================================================================================================================
# ============================================================ INIT ============================================================
# ==============================================================================================================================

status_mpu = 0          # 0 = none 
status_bmp = 0          # 1 = initialised
status_sd = 0           # 2 = callibrated
status_radio = 0        # 3 = error

status_i2c = 0          # 0 = none
status_uart = 0         # 1 = initialised
                        # 3 = error

# finite state machine that represents the state of the computer
periph = Periph()
computer = Machine(periph)
computer.setState(STATE_INIT)

# initialise the i2c communication bus
status_i2c = computer.initI2C()
if status_i2c == STATUS_ERROR:
    computer.setState(STATE_GND_ERROR)


if status_i2c == STATUS_SUCCESS_INIT:
    # sensors initial init
    
    if status_mpu != STATUS_ERROR: status_mpu = computer.initMPU()
    if status_bmp != STATUS_ERROR: status_bmp = computer.initBMP()
    
    print(status_i2c, status_mpu, status_bmp, status_sd, status_radio)
    
    # if all sensors initialised successfully, set the state to callibration
    if status_mpu == STATUS_SUCCESS_INIT and status_bmp == STATUS_SUCCESS_INIT and status_sd == STATUS_SUCCESS_INIT and status_radio == STATUS_SUCCESS_INIT:
        computer.setState(STATE_CALLIBRATION)
    # if any of the sensors failed to initialise, set the state to ground error
    else:
        computer.setState(STATE_GND_ERROR) 

# ==============================================================================================================================
# ============================================================ LOOP ============================================================
# ==============================================================================================================================

IDLE_DELAY_FOR_INIT = const(0)

number_except_loops = 0
MAX_NUMBER_ERROR_LOOPS_FOR_HARD_STATE_RESET = const(1)
LOOP_ERROR_DELAY = const(1)


number_error_loops = 0
number_error_loops_i2c = 0
number_error_loops_mpu = 0
number_error_loops_bmp = 0
number_error_loops_sd = 0
number_error_loops_radio = 0
MAX_NUMBER_ERROR_LOOPS_FOR_RESET_SENSOR = const(10)

i = 0
while True:
    try:
        # =================================================================================================================
        # ================================================= BORING STATES =================================================
        # =================================================================================================================

        # ====================================================== IDLE ======================================================
        if computer.state == STATE_IDLE:
            utime.sleep(IDLE_DELAY_FOR_INIT)
            computer.setState(STATE_INIT)
            pass
        
        # ====================================================== INIT ======================================================
        elif computer.state == STATE_INIT:
            # initialize the sensors
            
            print(status_i2c)
            
            if (status_i2c != STATUS_ERROR) and (status_i2c != STATUS_SUCCESS_INIT):
                status_i2c = computer.initI2C()
                if status_i2c == STATUS_ERROR:
                    computer.setState(STATE_GND_ERROR)


            # if not initialised, initialise the sensors
            if status_i2c == STATUS_SUCCESS_INIT:
                if (status_mpu != STATUS_ERROR) and (status_mpu != STATUS_SUCCESS_INIT): status_mpu = computer.initMPU()
                if (status_bmp != STATUS_ERROR) and (status_bmp != STATUS_SUCCESS_INIT): status_bmp = computer.initBMP()
                if (status_sd != STATUS_ERROR) and (status_sd != STATUS_SUCCESS_INIT): status_sd = computer.initSD()
                if (status_radio != STATUS_ERROR) and (status_radio != STATUS_SUCCESS_INIT): status_radio = computer.initRADIO()

            # if all sensors initialised successfully, set the state to callibration
            if status_mpu == STATUS_SUCCESS_INIT and status_bmp == STATUS_SUCCESS_INIT and status_sd == STATUS_SUCCESS_INIT and status_radio == STATUS_SUCCESS_INIT:
                computer.setState(STATE_CALLIBRATION)
            # if any of the sensors failed to initialise, set the state to ground error
            else:
                computer.setState(STATE_GND_ERROR) 

            pass
        
        
        # ===================================================== CALLIB =====================================================
        elif computer.state == STATE_CALLIBRATION:
            # callibrate the sensors 

            # if not callibrated, callibrate the sensors
            if (status_mpu != STATUS_ERROR) and (status_mpu != STATUS_SUCCESS_CALLIB): status_mpu = computer.callibMPU()
            if (status_bmp != STATUS_ERROR) and (status_bmp != STATUS_SUCCESS_CALLIB): status_bmp = computer.callibBMP()
            if (status_sd != STATUS_ERROR) and (status_sd != STATUS_SUCCESS_CALLIB): status_sd = computer.callibSD()
            if (status_radio != STATUS_ERROR) and (status_radio != STATUS_SUCCESS_CALLIB): status_radio = computer.callibRADIO()
            
            # if all sensors initialised successfully, set the state to callibration
            if status_mpu == STATUS_SUCCESS_CALLIB and status_bmp == STATUS_SUCCESS_CALLIB and status_sd == STATUS_SUCCESS_CALLIB and status_radio == STATUS_SUCCESS_CALLIB:
                computer.setState(STATE_READY)
            # if any of the sensors failed to initialise, set the state to ground error
            else:
                computer.setState(STATE_GND_ERROR) 
                print("Error during callibration")
            pass
            
            
        # =================================================================================================================
        # ================================================== GOOD STATES ==================================================
        # =================================================================================================================
        if computer.state == STATE_READY or computer.state == STATE_ASCENT or computer.state == STATE_DESCENT or computer.state == STATE_LANDED:
            pass
        
        
        # ===================================================== READY =====================================================
        elif computer.state == STATE_READY:
            # ready to launch

            if computer.detect_ascent():
                computer.setState(STATE_ASCENT)
                computer.setTimeLaunch(utime.time_ns())

            pass

        # ===================================================== ASCENT =====================================================
        elif computer.state == STATE_ASCENT:
            # rocket is ascending

            if computer.detect_apogee():
                computer.setState(STATE_DESCENT)
                computer.setTimeApogee(utime.time_ns())
            pass
        
        # ==================================================== DESCENT ====================================================
        elif computer.state == STATE_DESCENT:
            # rocket is descending

            # check for events
            if computer.detect_event1(): 
                flag_triggered_event_1 = computer.trigger_event1()
                if flag_triggered_event_1:
                    computer.setEvent1(True)
            
            if computer.detect_event2():
                flag_triggered_event_2 = computer.trigger_event2()
                if flag_triggered_event_2:
                    computer.setEvent2(True)

            # check if the rocket has landed
            if computer.detect_landed():
                computer.setState(STATE_LANDED)
                computer.setTimeLanded(utime.time_ns())
        
            pass
        
        # ==================================================== LANDED ====================================================
        elif computer.state == STATE_LANDED:
            # rocket has landed
            pass
        

        # =================================================================================================================
        # ===================================================== ERROR =====================================================
        # =================================================================================================================
        
        elif computer.state == STATE_GND_ERROR:
            if status_mpu == STATUS_ERROR:
                number_error_loops_mpu += 1
                print("MPU error, count {}".format(number_error_loops_mpu))
                
                if number_error_loops_mpu >= MAX_NUMBER_ERROR_LOOP_FOR_RESET_SENSOR:
                    print("{} loop errors. Resetting MPU".format(MAX_NUMBER_ERROR_LOOPS_FOR_RESET_SENSOR))
                    status_mpu = STATUS_NONE
                    number_error_loops_mpu = 0
                    computer.setState(STATE_INIT)
            
            if status_bmp == STATUS_ERROR:
                number_error_loops_bmp += 1
                print("BMP error, count {}".format(number_error_loops_bmp))
            
                if number_error_loops_bmp >= MAX_NUMBER_ERROR_LOOP_FOR_RESET_SENSOR:
                    print("{} loop errors. Resetting BMP".format(MAX_NUMBER_ERROR_LOOPS_FOR_RESET_SENSOR))
                    status_bmp = STATUS_NONE
                    number_error_loops_bmp = 0
                    computer.setState(STATE_INIT)
        
            if status_sd == STATUS_ERROR:
                number_error_loops_sd += 1
                print("SD error, count {}".format(number_error_loops_sd))
                if number_error_loops_sd >= MAX_NUMBER_ERROR_LOOP_FOR_RESET_SENSOR:
                    print("{} loop errors. Resetting SD".format(MAX_NUMBER_ERROR_LOOPS_FOR_RESET_SENSOR))
                    status_sd = STATUS_NONE
                    number_error_loops_sd = 0
                    computer.setState(STATE_INIT)
                    
            if status_radio == STATUS_ERROR:
                number_error_loops_radio += 1
                print("Radio error, count {}".format(number_error_loops_radio))
                if number_error_loops_radio >= MAX_NUMBER_ERROR_LOOP_FOR_RESET_SENSOR:
                    print("{} loop errors. Resetting RADIO".format(MAX_NUMBER_ERROR_LOOPS_FOR_RESET_SENSOR))
                    status_radio = STATUS_NONE
                    number_error_loops_radio = 0
                    computer.setState(STATE_INIT)
                
            if status_i2c == STATUS_ERROR:
                number_error_loops_i2c += 1
                print("I2C error, count {}".format(number_error_loops_i2c))
                
                if number_error_loops_i2c >= MAX_NUMBER_ERROR_LOOP_FOR_RESET_SENSOR:
                    print("{} loop errors. Resetting I2C".format(MAX_NUMBER_ERROR_LOOP_FOR_RESET))
                    status_i2c = STATUS_NONE
                    number_error_loops_i2c = 0
                    computer.setState(STATE_INIT)
            
            
            number_error_loops += 1
            if number_error_loops >= MAX_NUMBER_ERROR_LOOPS_FOR_HARD_STATE_RESET:
                print("{} loop errors. Hard state reset".format(MAX_NUMBER_ERROR_LOOPS_FOR_HARD_STATE_RESET))
                computer.setState(STATE_IDLE)
                number_error_loops = 0
                
                status_mpu = STATUS_NONE
                status_bmp = STATUS_NONE
                status_sd = STATUS_NONE
                status_radio = STATUS_NONE
    
            pass

        else:
            # error
            computer.setState(STATE_GND_ERROR) 
            pass

        i += 1
        print("loop {} | STATE {} \t || MPU {} | BMP {} | SD {} | RADIO {} \t || LAUNCH {} | APOGEE {} | EVENT1 {}  EVENT2 {} | LANDED"
              .format(i, computer.state, status_mpu, status_bmp, status_sd, status_radio, computer.launch, computer.apogee, computer.event1, computer.event2, computer.landed))
        print(computer.BMP.read(), computer.MPU.read())
        utime.sleep(computer.dt)

    except Exception as e:
        print("Error during loop:", e)
        computer.setState(STATE_GND_ERROR)
        utime.sleep(LOOP_ERROR_DELAY)
        
        number_except_loops += 1
        if number_except_loops >= MAX_NUMBER_ERROR_LOOPS_FOR_HARD_STATE_RESET:
            print("{} loop errors. Hard state reset".format(MAX_NUMBER_ERROR_LOOPS_FOR_HARD_STATE_RESET))
            computer.setState(STATE_IDLE)
            number_except_loops = 0
            
            status_mpu = STATUS_NONE
            status_bmp = STATUS_NONE
            status_sd = STATUS_NONE
            status_radio = STATUS_NONE
                
        pass



