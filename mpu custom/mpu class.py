
MPU6050_ADDRESS_AD0_LOW = const(0x68)
MPU6050_ADDRESS_AD0_HIGH = const(0x69)
MPU6050_DEFAULT_ADDRESS = const(MPU6050_ADDRESS_AD0_LOW)

SELF_TEST_X = const(13)
SELF_TEST_Y = const(14)
SELF_TEST_Z = const(15)
SELF_TEST_A = const(16)

SMPLRT_DIV = const(25)
CONFIG = const(26)
GYRO_CONFIG = const(27)
ACCEL_CONFIG = const(28)

ACCEL_XOUT_H = const(59)
ACCEL_XOUT_L = const(60)
ACCEL_YOUT_H = const(61)
ACCEL_YOUT_L = const(62)
ACCEL_ZOUT_H = const(63)
ACCEL_ZOUT_L = const(64)
TEMP_OUT_H = const(65)
TEMP_OUT_L = const(66)
GYRO_XOUT_H = const(67)
GYRO_XOUT_L = const(68)
GYRO_YOUT_H = const(69)
GYRO_YOUT_L = const(70)
GYRO_ZOUT_H = const(71)
GYRO_ZOUT_L = const(72)

PWR_MGMT_1 = const(107)
PWR_MGMT_2 = const(108)
WHO_AM_I = const(117)


class MPU6050: 
    def __init__(self, adr, i2c) -> None:
        self.i2c = i2c
        self.adr = adr
        pass
    
    def getDeviceID(self):
        return self.i2c.readfrom_mem(self.adr, WHO_AM_I, 1)[0]

    def testConnection(self):
        return self.getDeviceID() == 0x68
    
    @property
    def fullScaleGyroRange(self):
        return self.i2c.readfrom_mem(self.adr, GYRO_CONFIG, 1)[0] & 0x18

    @fullScaleGyroRange.setter
    def setFullScaleGyroRange(self, range):
        self.i2c.writeto_mem(self.adr, GYRO_CONFIG, range)
    
    @property
    def fullScaleAccelRange(self):
        return self.i2c.readfrom_mem(self.adr, ACCEL_CONFIG, 1)[0] & 0x18 

    @fullScaleAccelRange.setter
    def setFullScaleAccelRange(self, range):
        self.i2c.writeto_mem(self.adr, ACCEL_CONFIG, range)

    def getAcceleration(self):
        return
    

# class MPU6050_Base {
#     public:
#         MPU6050_Base(uint8_t address=MPU6050_DEFAULT_ADDRESS, void *wireObj=0);

#         void initialize();

#         // AUX_VDDIO register
#         uint8_t getAuxVDDIOLevel();
#         void setAuxVDDIOLevel(uint8_t level);

#         // SMPLRT_DIV register
#         uint8_t getRate();
#         void setRate(uint8_t rate);

#         // CONFIG register
#         uint8_t getExternalFrameSync();
#         void setExternalFrameSync(uint8_t sync);
#         uint8_t getDLPFMode();
#         void setDLPFMode(uint8_t bandwidth);

#         // GYRO_CONFIG register
#         uint8_t getFullScaleGyroRange();
#         void setFullScaleGyroRange(uint8_t range);

#         // SELF_TEST registers
#         uint8_t getAccelXSelfTestFactoryTrim();
#         uint8_t getAccelYSelfTestFactoryTrim();
#         uint8_t getAccelZSelfTestFactoryTrim();

#         uint8_t getGyroXSelfTestFactoryTrim();
#         uint8_t getGyroYSelfTestFactoryTrim();
#         uint8_t getGyroZSelfTestFactoryTrim();

#         // ACCEL_CONFIG register
#         bool getAccelXSelfTest();
#         void setAccelXSelfTest(bool enabled);
#         bool getAccelYSelfTest();
#         void setAccelYSelfTest(bool enabled);
#         bool getAccelZSelfTest();
#         void setAccelZSelfTest(bool enabled);
#         uint8_t getFullScaleAccelRange();
#         void setFullScaleAccelRange(uint8_t range);
#         uint8_t getDHPFMode();
#         void setDHPFMode(uint8_t mode);

#         // FF_THR register
#         uint8_t getFreefallDetectionThreshold();
#         void setFreefallDetectionThreshold(uint8_t threshold);

#         // FF_DUR register
#         uint8_t getFreefallDetectionDuration();
#         void setFreefallDetectionDuration(uint8_t duration);

#         // MOT_THR register
#         uint8_t getMotionDetectionThreshold();
#         void setMotionDetectionThreshold(uint8_t threshold);

#         // MOT_DUR register
#         uint8_t getMotionDetectionDuration();
#         void setMotionDetectionDuration(uint8_t duration);

#         // ZRMOT_THR register
#         uint8_t getZeroMotionDetectionThreshold();
#         void setZeroMotionDetectionThreshold(uint8_t threshold);

#         // ZRMOT_DUR register
#         uint8_t getZeroMotionDetectionDuration();
#         void setZeroMotionDetectionDuration(uint8_t duration);

#         // INT_STATUS register
#         uint8_t getIntStatus();
#         bool getIntFreefallStatus();
#         bool getIntMotionStatus();
#         bool getIntZeroMotionStatus();

#         // ACCEL_*OUT_* registers
#         void getMotion9(int16_t* ax, int16_t* ay, int16_t* az, int16_t* gx, int16_t* gy, int16_t* gz, int16_t* mx, int16_t* my, int16_t* mz);
#         void getMotion6(int16_t* ax, int16_t* ay, int16_t* az, int16_t* gx, int16_t* gy, int16_t* gz);
#         void getAcceleration(int16_t* x, int16_t* y, int16_t* z);
#         int16_t getAccelerationX();
#         int16_t getAccelerationY();
#         int16_t getAccelerationZ();

#         // TEMP_OUT_* registers
#         int16_t getTemperature();

#         // GYRO_*OUT_* registers
#         void getRotation(int16_t* x, int16_t* y, int16_t* z);
#         int16_t getRotationX();
#         int16_t getRotationY();
#         int16_t getRotationZ();

#         // EXT_SENS_DATA_* registers
#         uint8_t getExternalSensorByte(int position);
#         uint16_t getExternalSensorWord(int position);
#         uint32_t getExternalSensorDWord(int position);

#         // MOT_DETECT_STATUS register
#         uint8_t getMotionStatus();
#         bool getXNegMotionDetected();
#         bool getXPosMotionDetected();
#         bool getYNegMotionDetected();
#         bool getYPosMotionDetected();
#         bool getZNegMotionDetected();
#         bool getZPosMotionDetected();
#         bool getZeroMotionDetected();

#         // I2C_SLV*_DO register
#         void setSlaveOutputByte(uint8_t num, uint8_t data);

#         // I2C_MST_DELAY_CTRL register
#         bool getExternalShadowDelayEnabled();
#         void setExternalShadowDelayEnabled(bool enabled);
#         bool getSlaveDelayEnabled(uint8_t num);
#         void setSlaveDelayEnabled(uint8_t num, bool enabled);

#         // SIGNAL_PATH_RESET register
#         void resetGyroscopePath();
#         void resetAccelerometerPath();
#         void resetTemperaturePath();

#         // MOT_DETECT_CTRL register
#         uint8_t getAccelerometerPowerOnDelay();
#         void setAccelerometerPowerOnDelay(uint8_t delay);
#         uint8_t getFreefallDetectionCounterDecrement();
#         void setFreefallDetectionCounterDecrement(uint8_t decrement);
#         uint8_t getMotionDetectionCounterDecrement();
#         void setMotionDetectionCounterDecrement(uint8_t decrement);

#         // USER_CTRL register
#         void resetI2CMaster();
#         void resetSensors();

#         // PWR_MGMT_1 register
#         void reset();
#         bool getSleepEnabled();
#         void setSleepEnabled(bool enabled);
#         bool getWakeCycleEnabled();
#         void setWakeCycleEnabled(bool enabled);
#         bool getTempSensorEnabled();
#         void setTempSensorEnabled(bool enabled);
#         uint8_t getClockSource();
#         void setClockSource(uint8_t source);

#         // PWR_MGMT_2 register
#         uint8_t getWakeFrequency();
#         void setWakeFrequency(uint8_t frequency);
#         bool getStandbyXAccelEnabled();
#         void setStandbyXAccelEnabled(bool enabled);
#         bool getStandbyYAccelEnabled();
#         void setStandbyYAccelEnabled(bool enabled);
#         bool getStandbyZAccelEnabled();
#         void setStandbyZAccelEnabled(bool enabled);
#         bool getStandbyXGyroEnabled();
#         void setStandbyXGyroEnabled(bool enabled);
#         bool getStandbyYGyroEnabled();
#         void setStandbyYGyroEnabled(bool enabled);
#         bool getStandbyZGyroEnabled();
#         void setStandbyZGyroEnabled(bool enabled);

#         // WHO_AM_I register
#         uint8_t getDeviceID();
#         void setDeviceID(uint8_t id);
        
#         // ======== UNDOCUMENTED/DMP REGISTERS/METHODS ========
        
#         // XG_OFFS_TC register
#         uint8_t getOTPBankValid();
#         void setOTPBankValid(bool enabled);
#         int8_t getXGyroOffsetTC();
#         void setXGyroOffsetTC(int8_t offset);

#         // YG_OFFS_TC register
#         int8_t getYGyroOffsetTC();
#         void setYGyroOffsetTC(int8_t offset);

#         // ZG_OFFS_TC register
#         int8_t getZGyroOffsetTC();
#         void setZGyroOffsetTC(int8_t offset);

#         // X_FINE_GAIN register
#         int8_t getXFineGain();
#         void setXFineGain(int8_t gain);

#         // Y_FINE_GAIN register
#         int8_t getYFineGain();
#         void setYFineGain(int8_t gain);

#         // Z_FINE_GAIN register
#         int8_t getZFineGain();
#         void setZFineGain(int8_t gain);

#         // XA_OFFS_* registers
#         int16_t getXAccelOffset();
#         void setXAccelOffset(int16_t offset);

#         // YA_OFFS_* register
#         int16_t getYAccelOffset();
#         void setYAccelOffset(int16_t offset);

#         // ZA_OFFS_* register
#         int16_t getZAccelOffset();
#         void setZAccelOffset(int16_t offset);

#         // XG_OFFS_USR* registers
#         int16_t getXGyroOffset();
#         void setXGyroOffset(int16_t offset);

#         // YG_OFFS_USR* register
#         int16_t getYGyroOffset();
#         void setYGyroOffset(int16_t offset);

#         // ZG_OFFS_USR* register
#         int16_t getZGyroOffset();
#         void setZGyroOffset(int16_t offset);
        
        
#         // USER_CTRL register (DMP functions)
#         bool getDMPEnabled();
#         void setDMPEnabled(bool enabled);
#         void resetDMP();
        
#         // BANK_SEL register
#         void setMemoryBank(uint8_t bank, bool prefetchEnabled=false, bool userBank=false);
        
#         // MEM_START_ADDR register
#         void setMemoryStartAddress(uint8_t address);
        
#         // MEM_R_W register
#         uint8_t readMemoryByte();
#         void writeMemoryByte(uint8_t data);
#         void readMemoryBlock(uint8_t *data, uint16_t dataSize, uint8_t bank=0, uint8_t address=0);
#         bool writeMemoryBlock(const uint8_t *data, uint16_t dataSize, uint8_t bank=0, uint8_t address=0, bool verify=true, bool useProgMem=false);
#         bool writeProgMemoryBlock(const uint8_t *data, uint16_t dataSize, uint8_t bank=0, uint8_t address=0, bool verify=true);

#         bool writeDMPConfigurationSet(const uint8_t *data, uint16_t dataSize, bool useProgMem=false);
#         bool writeProgDMPConfigurationSet(const uint8_t *data, uint16_t dataSize);

#         // DMP_CFG_1 register
#         uint8_t getDMPConfig1();
#         void setDMPConfig1(uint8_t config);

#         // DMP_CFG_2 register
#         uint8_t getDMPConfig2();
#         void setDMPConfig2(uint8_t config);

# 		// Calibration Routines
# 		void CalibrateGyro(uint8_t Loops = 15); // Fine tune after setting offsets with less Loops.
# 		void CalibrateAccel(uint8_t Loops = 15);// Fine tune after setting offsets with less Loops.
# 		void PID(uint8_t ReadAddress, float kP,float kI, uint8_t Loops);  // Does the math
# 		void PrintActiveOffsets(); // See the results of the Calibration
# 		int16_t * GetActiveOffsets();

#     protected:
#         uint8_t devAddr;
#         void *wireObj;
#         uint8_t buffer[14];
#         uint32_t fifoTimeout = MPU6050_FIFO_DEFAULT_TIMEOUT;
    
#     private:
#         int16_t offsets[6];
# };
