import time
import socketio
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from Adafruit_BBIO.SPI import SPI
def LedMatrix8x8ClickInit():
     L_Spi1 = SPI(1,0)
     L_Spi1.mode = 0
     L_Spi1.writebytes([0x09, 0x00])
     L_Spi1.writebytes([0x0A, 0x01])
     L_Spi1.writebytes([0x0B, 0x07])
     L_Spi1.writebytes([0x0C, 0x01])
     return L_Spi1
def PrintDisplay(L_Spi1, DisplayList):
     L_Spi1.writebytes([0x01, DisplayList[0]])
     L_Spi1.writebytes([0x02, DisplayList[1]])
     L_Spi1.writebytes([0x03, DisplayList[2]])
     L_Spi1.writebytes([0x04, DisplayList[3]])
     L_Spi1.writebytes([0x05, DisplayList[4]])
     L_Spi1.writebytes([0x06, DisplayList[5]])
     L_Spi1.writebytes([0x07, DisplayList[6]])
     L_Spi1.writebytes([0x08, DisplayList[7]])

G_SmileyHappyFace = [0b00111100,
                     0b01000010,
                     0b10101001,
                     0b10000101,
                     0b10000101,
                     0b10101001,
                     0b01000010,
                     0b00111100]
G_ClearDisplay = [0b00000000,
                  0b00000000,
                  0b00000000,
                  0b00000000,
                  0b00000000,
                  0b00000000,
                  0b00000000,
                  0b00000000]
                  
G_Spi1 = LedMatrix8x8ClickInit()


# Setup
GPIO.setup("P9_15", GPIO.IN)
sio = socketio.Client()

@sio.event
def connect():
    print('Connection established.')

@sio.event
def disconnect():
    print('Disconnected from server.')

@sio.event
def CommandLight(RxData):
    print("Poll Recieved")
    if RxData["Buzzerctl"]:
        PWM.start("P8_19", 50)
        PWM.set_frequency("P8_19", 1000)
        time.sleep(0.3)
    else:
        PWM.stop("P8_19")
    if RxData["Relay1Ctl"]:
        PWM.start("P9_14", 50)
        PWM.set_frequency("P8_19", 1000)
        time.sleep(0.3)
    else:
        PWM.stop("P8_19")
    Data = {"ReadyStat":True, "Buzzerstat":False, "Data1":16}
    sio.emit('GetStatusLight', Data)
    print(RxData)

    
while True:
    try:
        sio.connect('http://192.168.72.118:5000')
        break
    except:
        print("Try to connect to the server.")
        pass

while True:    
    time.sleep(0.1)  # Short sleep to reduce CPU usage