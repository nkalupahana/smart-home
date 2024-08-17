from enum import Enum
from flask import Flask
from time import sleep
import json
from threading import Lock
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

GPIO.output(2, GPIO.HIGH)
GPIO.output(3, GPIO.HIGH)

app = Flask(__name__)
lock = Lock()

@app.route("/")
def index():
    return "Curtains server up"

# State from HomeKit is 0 - 100
@app.route("/set/<int:desired_state>")
def move_curtains(desired_state):
    with lock:
        state = get_state()
        delta = desired_state - state
        start_moving(delta)
        sleep(calculate_sleep(delta))
        stop_moving()
        set_state(desired_state)
    
    return "OK"

@app.route("/status")
def status():
    return json.dumps({"position": get_state()})

###

def get_state():
    try:
        with open("state.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0
    
def set_state(state):
    with open("state.txt", "w") as f:
        f.write(str(state))

def start_moving(delta):
    if delta > 0:
        GPIO.output(3, GPIO.LOW)
        GPIO.output(2, GPIO.HIGH)
    elif delta < 0:
        GPIO.output(3, GPIO.HIGH)
        GPIO.output(2, GPIO.LOW)
    else:
        return
    
def stop_moving():
    GPIO.output(2, GPIO.HIGH)
    GPIO.output(3, GPIO.HIGH)

HOMEKIT_TO_TIME_MULTIPLIER = 0.2
def calculate_sleep(delta):
    ret = abs(delta) * HOMEKIT_TO_TIME_MULTIPLIER
    # If we're going down, we need to sleep
    # a little less
    if delta < 0:
        ret -= 0.25

    return ret