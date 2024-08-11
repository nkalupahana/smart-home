from RPi.GPIO import GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

GPIO.output(2, GPIO.HIGH)
GPIO.output(3, GPIO.HIGH)

while True:
    key = input("u - up, d - down, q - quit: ")
    if key == 'u':
        GPIO.output(2, GPIO.LOW)
        GPIO.output(3, GPIO.HIGH)
    elif key == 'd':
        GPIO.output(2, GPIO.HIGH)
        GPIO.output(3, GPIO.LOW)
    elif key == 'q':
        break

    input("Press Enter to stop")
    GPIO.output(2, GPIO.HIGH)
    GPIO.output(3, GPIO.HIGH)