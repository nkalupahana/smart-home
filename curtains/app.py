from enum import Enum
from flask import Flask
from time import sleep
from threading import Lock
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

GPIO.output(2, GPIO.HIGH)
GPIO.output(3, GPIO.HIGH)

HOMEKIT_TO_TIME_MULTIPLIER = 0.1

app = Flask(__name__)
lock = Lock()

@app.route("/")
def index():
    return "Curtains server up"

# State from HomeKit is 0 - 100
@app.route("/set/<int:desired_state>")
def status(desired_state):
    with lock:
        state = get_state()
        delta = desired_state - state
        start_moving(delta)
        sleep(abs(delta) * HOMEKIT_TO_TIME_MULTIPLIER)
        stop_moving()
        set_state(desired_state)
    
    return "OK"

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