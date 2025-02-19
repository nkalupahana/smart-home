from functools import wraps
from flask import Flask, request
from time import time, sleep
import RPi.GPIO as GPIO
from dotenv import load_dotenv
import os

load_dotenv()

REED_SWITCH_PIN = 17
REMOTE_BUTTON_PIN = 18
DOOR_OPEN_TIME = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(REED_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(REMOTE_BUTTON_PIN, GPIO.OUT)

def push_remote_button():
    GPIO.output(REMOTE_BUTTON_PIN, GPIO.LOW)
    sleep(0.3)
    GPIO.output(REMOTE_BUTTON_PIN, GPIO.HIGH)


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")

        if api_key != os.environ["API_KEY"]:
            return {"success": False}, 403

        return f(*args, **kwargs)

    return decorated_function

app = Flask(__name__)
last_open_time = 0
last_close_time = 0

@app.route("/")
def index():
    return "Garage door server up"


@app.route("/open")
@require_api_key
def open_door():
    global last_open_time
    push_remote_button()
    last_open_time = time()
    return {"success": True}


@app.route("/close")
@require_api_key
def close_door():
    global last_close_time
    push_remote_button()
    last_close_time = time()
    return {"success": True}


@app.route("/status")
@require_api_key
def status():
    state = ""
    door_closed = GPIO.input(REED_SWITCH_PIN) == GPIO.LOW

    if door_closed:
        state = "CLOSED"
    else:
        if time() - last_open_time < DOOR_OPEN_TIME:
            state = "OPENING"
        elif time() - last_close_time < DOOR_OPEN_TIME:
            state = "CLOSING"
        else:
            state = "OPEN"

    return {"success": True, "state": state}
