#!/usr/bin/env python3
import os
import sys

import time
from flask import Flask, render_template, Response

# Raspberry Pi camera module (requires picamera package)
# from camera.testcamera import Camera
from camera.raspcamera import Camera
from battery.battery import Battery
sys.path.append(os.path.join(os.path.expanduser("~"), 'platform'))  # https://github.com/ArtemZaZ/file-organization
from configuration import robot  # platform.configuration.robot
from testsmodel.testrobot import Robot

app = Flask(__name__)
bat = Battery()


robotSpeed = 50


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
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/mouse/<cmd>')
def mouseCommand(cmd=None):
    cmd = cmd.split(',')
    print("cmd: ", cmd)
    if cmd[0] == 'press':
        if cmd[1] == 'up':
            robot.move(robotSpeed)
        elif cmd[1] == 'down':
            robot.move(-robotSpeed)
        elif cmd[1] == 'left':
            robot.rotate(-robotSpeed)
        elif cmd[1] == 'right':
            robot.rotate(robotSpeed)

    if cmd[0] == 'release':
        if cmd[1] == 'up':
            robot.move(0)
        elif cmd[1] == 'down':
            robot.move(0)
        elif cmd[1] == 'left':
            robot.rotate(0)
        elif cmd[1] == 'right':
            robot.rotate(0)
    return '', 200, {'Content-Type': 'text/plain'}


@app.route('/range/<value>')
def rangeValue(value=None):
    robot.setCamera(value / 50 - 1)
    return '', 200, {'Content-Type': 'text/plain'}


@app.route('/battery_charge')
def battery_charge():
    """  """
    return Response(genVoltage(Robot()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    robot.initializeAll()
    app.run(host='192.168.42.10', threaded=True, port=5000)
