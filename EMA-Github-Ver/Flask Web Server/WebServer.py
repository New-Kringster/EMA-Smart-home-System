from flask import Flask
from flask import render_template
from flask_socketio import SocketIO
from flask_socketio import emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
	return render_template('project.html')

@socketio.event
def Buzzering(RxData):
	if RxData == 'on':
		socketio.emit('Buzzering', RxData)
	if RxData == 'off':
		socketio.emit('Buzzering', RxData)

@socketio.event
def TempEvent(RxData):
        cleandata = f'{RxData['data']:.1f}'
        socketio.emit('Web_TempEvent', cleandata)
        print(f'Temp {cleandata} Receive Data from BBBW')

@socketio.event
def HumidEvent(RxData):
        cleandata = f'{RxData['data']:.1f}'
        socketio.emit('Web_HumidEvent', cleandata)
        print(f'Humid {cleandata} Receive Data from BBBW')

if __name__ == '__main__':
	app.run(host='192.168.72.221')
