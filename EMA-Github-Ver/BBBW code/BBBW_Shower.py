import time
import socketio
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC

import board
import busio
import digitalio
import adafruit_ssd1306
from board import SCL, SDA
from PIL import Image, ImageDraw, ImageFont

ADC.setup()
GPIO.setup("P8_17", GPIO.IN)


motion = False  
temperature = 30
shower = False
timer_active = False
duration = 0
sio = socketio.Client()


@sio.event
def connect():
    print('Connection established.')

@sio.event
def disconnect():
    print('Disconnected from server.')

@sio.event
def CommandFireMon(RxData):
    print("Poll Recieved")
    if RxData["Buzzerctl"]:
        PWM.start("P9_14", 50)
        PWM.set_frequency("P9_14", 800)
        time.sleep(0.3)
    else:
        PWM.stop("P9_14")
    Data = {"ReadyStat":True, "Buzzerstat":False, "Data1": shower, "Data2": duration}
    sio.emit('GetStatusFireMon', Data)
    print("Data sent")

def OLEDClickInit():
    Pin_DC = digitalio.DigitalInOut(board.P9_16)
    Pin_DC.direction = digitalio.Direction.OUTPUT
    Pin_DC.value = False
    Pin_RESET = digitalio.DigitalInOut(board.P9_23)
    Pin_RESET.direction = digitalio.Direction.OUTPUT
    Pin_RESET.value = True
    L_I2c = busio.I2C(SCL, SDA)
    return L_I2c

G_I2c = OLEDClickInit()
Display = adafruit_ssd1306.SSD1306_I2C(128, 64, G_I2c, addr=0x3C)
ImageObj = Image.new("1", (Display.width, Display.height))

Draw = ImageDraw.Draw(ImageObj)

while True:
    try:
        sio.connect('http://192.168.72.118:5000')
        break
    except:
        print("Try to connect to the server.")
        pass
    
while True:
    Draw.rectangle((42, 25, Display.width - 1, Display.height - 1 ), outline=1, fill=0)
    if GPIO.input("P8_17"):
        motion = True
        print("Motion is Detected")
    else:
        motion = False
        print("No Motion is Detected")
        
        
    DigitalValue = ADC.read("P9_40")
    if DigitalValue >= 0.00 and DigitalValue < 0.10:
        print("No Key is Pressed")
        
        
    elif DigitalValue > 0.16 and DigitalValue < 0.18:
        temperature += 0.5
        print(f"T6 Key is Pressed - Temperature: {temperature}°C")
        
        
    elif DigitalValue > 0.33 and DigitalValue < 0.35:
        temperature -= 0.5
        print(f"T5 Key is Pressed - Temperature: {temperature}°C")


    elif DigitalValue > 0.50 and DigitalValue < 0.52:
        if shower == False: 
            shower = True
            print("T4 Key is Pressed - Shower ON")
            

        else:
            print("T4 Key Pressed - Shower already ON.")
            
            
    elif DigitalValue > 0.67 and DigitalValue < 0.69:
        if shower == True: 
            shower = False
            duration = 0
            print("T3 Key is Pressed - Shower OFF")
        else:
            print("T3 Key Pressed - Shower already OFF.")
        
        
    elif DigitalValue > 0.84 and DigitalValue < 0.86:
        duration += 10 
        print(f"T2 Key is Pressed - Timer duration increased to {duration} seconds.")

            
    elif DigitalValue > 0.90 and DigitalValue < 1.10:
        if duration > 10: 
            duration -= 10
            print(f"T1 Key is Pressed - Timer duration decreased to {duration} seconds.")
        else:
            print("T1 Key is Pressed - Timer not active or cannot decrease further.")

    if shower == True and motion == True:
        duration -= 1
        if duration == 0:
            print("Timer expired!")
            timer_active = False
            PWM.start("P9_14", 50)
            PWM.set_frequency("P9_14", 523)
            time.sleep(0.5)
            PWM.set_frequency("P9_14", 587)
            time.sleep(0.5)
            PWM.set_frequency("P9_14", 659)
            time.sleep(0.5)
            PWM.stop("P9_14")
            shower == False
            print("Please turn off shower")
            print(f"Timer run out. Remaining: {duration:.1f} seconds")
        else:
            print(f"Timer active. Remaining: {duration:.1f} seconds")
    
    if shower == True:
        showerStatus = "On"
    else:
        showerStatus = "Off"
    
    Font = ImageFont.load_default()
    Draw.text((46, 25), f"Temp:{temperature:.1f}°C", font=Font, fill=1)
    Draw.text((46, 37), f"Duration:{duration}s", font=Font, fill=1)
    Draw.text((46, 50), f"Shower:{showerStatus}", font=Font, fill=1)
    Display.image(ImageObj)
    Display.show()

    time.sleep(0.1)