import socketio
import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM
import board
import busio
import digitalio
import adafruit_ssd1306
from board import SCL, SDA
from PIL import Image, ImageDraw, ImageFont

GPIO.setup('USR0', GPIO.OUT)    
ADC.setup()
sio = socketio.Client()

@sio.event
def connect():
    print('Connection established.')

@sio.event
def disconnect():
    print('Disconnected from server.')

@sio.event
def CommandEnergyMon(RxData):
    if RxData["Buzzerctl"]:
        PWM.start("P8_19", 50)
        PWM.set_frequency("P8_19", 800)
        time.sleep(0.3)
    else:
        PWM.stop("P8_19")
    Fridgepower = float(f'{AnalogValue * 100:.1f}')
    print("Fridgepower: %f" % (Fridgepower))
    Data = {"ReadyStat": True, "Data1": Fridgepower, "Buzzerstat": False, "Data2": fireStatus }
    sio.emit('GetStatusEnergyMon', Data)
    print("Data sent!")

def OLEDClickInit():
    Pin_DC = digitalio.DigitalInOut(board.P9_14)
    Pin_DC.direction = digitalio.Direction.OUTPUT
    Pin_DC.value = False
    Pin_RESET = digitalio.DigitalInOut(board.P9_12)
    Pin_RESET.direction = digitalio.Direction.OUTPUT
    Pin_RESET.value = True
    L_I2c = busio.I2C(SCL, SDA)
    return L_I2c
    
G_I2c = OLEDClickInit()
Display = adafruit_ssd1306.SSD1306_I2C(64, 32, G_I2c, addr=0x3C)
ImageObj = Image.new("1", (Display.width, Display.height))

OldDigitalValue = 0


while True:
    try:                         
        sio.connect('http://192.168.72.118:5000')    #Tries to connect. If successful, continue to next try statement.
        break
    except:
        print("Trying to connect to server")   #If cannot, try again
        time.sleep(0.2)
        pass
        
while True:
    try:
        NewDigitalValue = ADC.read("P9_39")
        FlameClickValue = ADC.read("P9_37")
        AnalogValue = (NewDigitalValue * 1.8)
        if FlameClickValue > 0.0022:
            fireStatus = True
        else:
            fireStatus = False
        print("AnalogValue: %f" % (AnalogValue))
        print("FlameClickValue: %f" % (FlameClickValue))
        print("Fire Status: %f" % (fireStatus))
        Draw = ImageDraw.Draw(ImageObj)
        Draw.rectangle((0, 0, Display.width - 1, Display.height - 1), outline=1, fill=0)
        Font = ImageFont.load_default()
        Text = f"{AnalogValue}"
        Draw.text((2, 10), Text, font=Font, fill=1)
        Display.image(ImageObj)
        Display.show()
        
        # if(AnalogValue > 1):
        #     PWM.start("P8_19", 50)
        #     PWM.set_frequency("P8_19", 523)
        #     time.sleep(0.5)
        #     PWM.stop("P8_19")
        #     print('Data sent!')
    except:
        print('Unable to transmit data.')
        pass
    time.sleep(1)
