import time
import socketio
import board
import adafruit_bme680
import Adafruit_BBIO.PWM as PWM
from Adafruit_BBIO.SPI import SPI
import Adafruit_BBIO.GPIO as GPIO
sio = socketio.Client()

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

GPIO.setup("P8_17", GPIO.IN)

@sio.event
def connect():
    print('Connection established.')

@sio.event
def disconnect():
    print('Disconnected from server.')
    
i2c = board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, 0x77)

#Singapore mean pressure (hPa) at sea level
bme680.sea_level_pressure = 1008.5

#Calibrate the temperature sensor value
temperature_offset = -5

left = [0b10000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000]
    
right = [0b00000001,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000]

blank = [0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000]
    
G_Spi1 = LedMatrix8x8ClickInit()
@sio.event
def CommandCC(RxData):
    if RxData["Relay1ctl"]:
        PrintDisplay(G_Spi1, left)
        print("left")
    if RxData["Relayctl2"]:
        PrintDisplay(G_Spi1, right)
        print("Right")
    if RxData["Relay1ctl"] == False and RxData["Relayctl2"] == False:
        PrintDisplay(G_Spi1, blank)
        print("All Off")
    if RxData["Buzzerctl"]:
        PWM.start("P9_16", 50)
        PWM.set_frequency("P8_19", 800)
        time.sleep(0.3)
    else:
        PWM.stop("P8_19")
    print("Poll Recieved")
    humidity = f"{bme680.relative_humidity:.1f}"
    tempreature = f"{(bme680.temperature + temperature_offset):.1f}"
    print(tempreature)
    Data = {"ReadyStat":True, "Data1":float(humidity), "Data2":float(tempreature),"Data3":GPIO.input("P8_17"), "Buzzerstat":False}
    sio.emit('GetStatusCC', Data)
    print(RxData)

while True:
    try:
        sio.connect('http://192.168.72.118:5000')
        break
    except:
        print("Try to connect to the server.")
        pass
    time.sleep(0.2)
    
    
while True:
    time.sleep(0.5)