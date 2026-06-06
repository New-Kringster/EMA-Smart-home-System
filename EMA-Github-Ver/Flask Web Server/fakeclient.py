# Eg of how SocketIO works:
#
# Sender side...
#
#   sio.emit('SendData', DATA)
#
# this basically means, send [DATA] to the function SendData on the reciever side.
#
# Reciever side...
#
#   @sio.event
#   def SendData(DATA):
#       [do stuff with the DATA]
#
# now that the reciever recieved the [DATA] you can do stuff with the data you got inside of the function.

import time
import socketio
import json
import random
import sys
# when running on pc do remember to pip install "python-socketio[client]"
Buzzerstats = False


sio = socketio.Client()

@sio.event
def connect():
    print('Connection established.')

@sio.event
def disconnect():
    print('Disconnected from server.')
#Don't touch anything above this


@sio.event
def CommandEnergyMon(RxData):
    print("Poll Recieved")
    print("Poll Recieved")
    fire = False
    randomoutof5 = random.randint(1,10)
    if randomoutof5 == 6:
        fire = True
        print("Fire Activated")
    Fridgepower = random.randint(30,120)
    Data = {"ReadyStat":True, "Data1":Fridgepower, "Buzzerstat":Buzzerstats,"Data2": fire}
    sio.emit('GetStatusEnergyMon', Data)
    print(RxData)

@sio.event
def CommandCC(RxData):
    print("Poll Recieved")
    humidity = random.randint(50,79)
    tempreature = random.randint(20,29)
    presence = True
    Data = {"ReadyStat":True, "Data1":humidity, "Data2":tempreature, "Buzzerstat":Buzzerstats, "Data3":presence}
    sio.emit('GetStatusCC', Data)
    print(RxData)

@sio.event
def CommandLight(RxData):
    print("Poll Recieved")
    lightspower = random.randint(10,15)
    Data = {"ReadyStat":True, "Buzzerstat":Buzzerstats, "Data1":lightspower}
    sio.emit('GetStatusLight', Data)
    print(RxData)

@sio.event
def CommandFireMon(RxData):
    Data = {"ReadyStat":True, "Buzzerstat":Buzzerstats, "Data1":True, "Data2":"Shwer time left"}
    sio.emit('GetStatusFireMon', Data)
    print(RxData)

@sio.event
def CommandIntrusionMon(RxData):
    print("Poll Recieved")
    randomoutof5 = random.randint(1,10)
    knocking = False
    door = False
    if randomoutof5 == 4:
        knocking = True
        print("Knock Activated")
    if randomoutof5 == 3:
        door = True
        print("DoorZ")
    Data = {"ReadyStat":True, "Buzzerstat":Buzzerstats, "Data5": knocking, "Data3": door}
    sio.emit('GetStatusIntrusionMon', Data)
    print(RxData)
#spits out whatever was sent to Buzzering SocketIO event (you can change the name to fit urs)
    
while True:
    try:
        sio.connect('http://127.0.0.1:5000')
        break
    except:
        time.sleep(0.5)
        print("Try to connect to the server.")
        pass

#Don't touch anything in this loop



    
