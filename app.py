#!/usr/bin/env python3
from importlib import import_module
import os
from flask import Flask, render_template, Response

from camera.testcamera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera.raspcamera import Camera


app = Flask(__name__)


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


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
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


if __name__ == '__main__':
    app.run(host='127.1.0.1', threaded=True, port=5000)
