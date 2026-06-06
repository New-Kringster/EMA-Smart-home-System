import time
import socketio
import Adafruit_BBIO.PWM as PWM # For Buzzer
from Adafruit_BBIO.SPI import SPI  #For LED Matrix
import Adafruit_BBIO.GPIO as GPIO # For Motion
import Adafruit_BBIO.GPIO as GPIO  #For Reed

GPIO.setup("P8_10", GPIO.IN)# REED
GPIO.setup("P9_23", GPIO.OUT)
GPIO.setup("P9_41", GPIO.IN)

GPIO.output("P9_23", GPIO.HIGH)


sio = socketio.Client()
ReedCheck = False
VibraCheck = False
testnum = 0

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")
    
@sio.event
def CommandIntrusionMon(RxData):
    print("Poll Recieved")
    if RxData["Buzzerctl"]:
        PWM.start("P9_14", 50)
        PWM.set_frequency("P9_14", 800)
        time.sleep(0.3)
    else:
        PWM.stop("P9_14")
    # if RxData["KnockBuzCtl"]:
    #     #knockbuzz
    # if RxData["DisplayCtl"]:
    #     #Display
    Data = {"ReadyStat":True, "Buzzerstat":False, "Data1":False, "Data5": VibraCheck, "Data3": ReedCheck}
    sio.emit('GetStatusIntrusionMon', Data)
    print(RxData)

while True:
    try:
        sio.connect('http://192.168.72.118:5000')
        break
    except:
        print("Try to connect to the server.")
        pass

while True:
    if GPIO.input("P8_10"):
        ReedCheck = False
    else:
        print("No Magnet is Detected")
        ReedCheck = True
    if testnum > 1000:
        testnum = 0
        VibraCheck = False
        print("Stopped")
    if VibraCheck:
        print()
        testnum = testnum + 1
        print("Vibration is Detected")
    if GPIO.input("P9_41"):
        VibraCheck = True