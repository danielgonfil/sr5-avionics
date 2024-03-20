from micropython import const

PIN_RED_LED = const(18)
PIN_YELLOW_LED = const(19)
PIN_GREEN_LED = const(20)

PIN_SCL = const(1)
PIN_SDA = const(0)

CORRECT_I2C = [56, 104, 119]
MPU_ADDRESS = const(104)
BMP_ADDRESS = const(119)

SD_SCK = const(10)
SD_MOSI = const(11)
SD_MISO = const(8)
SD_CS = const(9)

HC_RX = const(5)
HC_TX = const(4)

STATE_IDLE = const(1)
STATE_CALLIBRATION = const(2)
STATE_GND_ERROR = const(3)
STATE_READY = const(4)
STATE_FLIGHT = const(5)
STATE_ASCENT = const(6)
STATE_DESCENT = const(7)
STATE_LANDED = const(8)

# opertaions frequency / sampling rate
READY_DT = 1
ASCENT_DT = 0.1
DESCENT_DT = 0.1
LANDED_DT = 1
