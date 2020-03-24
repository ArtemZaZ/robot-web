#!/usr/bin/env python3
from importlib import import_module
import os
from flask import Flask, render_template, Response
import threading
from camera.testcamera import Camera
from testsmodel.testrobot import Robot
from battery.battery import Battery
import time

# Raspberry Pi camera module (requires picamera package)
# from camera.raspcamera import Camera


app = Flask(__name__)
bat = Battery()
cam = None


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('wjoystick.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def genVoltage(robot):
    """ Переодически отправляем напряжение """
    while True:
        frame = bat.getImage(voltage=robot.voltage)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(1)


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    global cam
    cam = Camera()
    return Response(gen(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/battery_charge')
def battery_charge():
    """  """
    return Response(genVoltage(Robot()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/mouse/<cmd>')
def mouseCommand(cmd=None):
    cmd = cmd.split(',')
    print("cmd: ", cmd)
    return '', 200, {'Content-Type': 'text/plain'}


@app.route('/range/<value>')
def rangeValue(value=None):
    print("value: ", value)
    return '', 200, {'Content-Type': 'text/plain'}


def onlineThread():
    while True:
        if cam is not None:
            print(cam.thread is None)
        time.sleep(1)


if __name__ == '__main__':
    threading.Thread(target=onlineThread, daemon=True).start()
    app.run(host='192.168.1.187', threaded=True, port=5000)

