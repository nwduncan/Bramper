import RPi.GPIO as GPIO
import time
from threading import Timer

pin = 19    # pin11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

shooting = False

def release(length):
    timer1 = Timer(length, end)
    GPIO.output(pin, GPIO.HIGH)
    shooting = True
    timer1.start()

def end():
    GPIO.output(pin, GPIO.LOW)
    shooting = False


# def release(length):
#     GPIO.output(pin, GPIO.HIGH)
#     time.sleep(length)
#     GPIO.output(pin, GPIO.LOW)


def destroy():
    GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()
