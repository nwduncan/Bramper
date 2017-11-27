import screens
import time
import RPi.GPIO as GPIO

# button variables
PIN_UP = 5
PIN_DOWN = 6
PIN_LEFT = 13
PIN_RIGHT = 19
PIN_SELECT = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_left, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_right, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_select, GPIO.IN, pull_up_down=GPIO.PUD_UP)

screen_settings = screens.Settings("shutterspeed2", "iso", "f-number")

while True:
    if GPIO.input(PIN_UP) == GPIO.LOW:
        screen_settings.up()
        time.sleep(0.5)
    elif GPIO.input(PIN_DOWN) == GPIO.LOW:
        screen_settings.down()
        time.sleep(0.5)
    elif GPIO.input(PIN_LEFT) == GPIO.LOW:
        screen_settings.left()
        time.sleep(0.5)
    elif GPIO.input(PIN_RIGHT) == GPIO.LOW:
        screen_settings.right()
        time.sleep(0.5)
    elif GPIO.input(PIN_SELECT) == GPIO.LOW:
        screen_settings.submit()
        time.sleep(0.5)
    else:
        pass
