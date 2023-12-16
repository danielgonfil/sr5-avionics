# **Project Components**
- **Microcontroller:** Raspberry PICO (2-4 in total)
- **Gyro – Accelerometer:** MPU-6050
- **Barometer:** BMP-280
- **Camera:** Arducam 2MP SPI or ESP32-CAM (transmits images using Wi-Fi)
- **Telemetry Radio:** HC-12 (433MHz)
- **Video Transmission Wi-Fi:** ESP01S (1-2 in total)
## **Components’ Interaction Scheme**
1. ### **1. Live Video Recording and Transmission**
Typical 433MHz LoRa modules have lower bitrates (< 300kbps), insufficient for high-quality live video transmission (High quality 960x540 or HD720: 1200-1500 kbps and 1500-4000, respectively). Hence, Wi-Fi is chosen.

**Issue:** FSPL for 2.4GHz is 95dB for 700m, while FSPL for 433Mhz at the same distance is 80dB.

ESP01S output power is 17+-2 dBm, and receiving sensitivity is -90dBm at 6Mbps. A high-gain antenna on the ground is necessary to receive the signal.
#### **Options:**
1. **Option 1:** Sending telemetry via HC-12, recording video with Arducam 2MP SPI (saved on SD card), and transmitting using ESP-01 to the ground. Received on the ground with PICO, then displayed on the computer.

![](/images/comp1.png)

1. **Option 2:** Sending telemetry via HC-12, recording and sending video using ESP32-CAM, and receiving on the ground with PICO. Displayed on the computer.

![](/images/comp2.png)

### **2. Barometer and Gyro-Accelerometers**
Both directly interact with PICO. Measurements are stored on SD card and sent via HC-12 to the ground (could also be sent via Wi-Fi in parallel to video). Both can trigger events (e.g., servo-motors opening the nose-cone). Accelerometer’s data can be integrated for velocity and height comparison with barometer readings.
### **3. PICO’s State Indicators**
A button for powering the circuit, LEDs, and buzzers are added for easy verification of the current state of the circuit and PICO. The buzzer signals sleep-mode, powering up, reset, errors, start and end of Wi-Fi and radio communications. LEDs duplicate some of those signals (possibly several LEDs in different parts of the circuit). A log of all events during flight may also be stored on the SD card.


### **4. Servo Motors**
To do with structure team
1. ### **5. Antenna**
To do

