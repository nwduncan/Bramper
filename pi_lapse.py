import screens
import time
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD

# wiring variables
LCD_RS = 25
LCD_EN = 24
LCD_D4 = 23
LCD_D5 = 17
LCD_D6 = 18
LCD_D7 = 22

# lcd variables
LCD_BL = 4
LCD_COL = 16
LCD_ROWS = 2

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

lcd = LCD.Adafruit_CharLCD(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7, LCD_COL, LCD_ROWS, LCD_BL)
screen_settings = screens.Settings("shutterspeed2", "iso", "f-number", lcd)

active = screen_settings

def make_active(screen):
    global active
    active = screen
    active.set_active()


while True:
    if GPIO.input(PIN_UP) == GPIO.LOW:
        active.up()
        time.sleep(0.5)
    elif GPIO.input(PIN_DOWN) == GPIO.LOW:
        active.down()
        time.sleep(0.5)
    elif GPIO.input(PIN_LEFT) == GPIO.LOW:
        active.left()
        time.sleep(0.5)
    elif GPIO.input(PIN_RIGHT) == GPIO.LOW:
        active.right()
        time.sleep(0.5)
    elif GPIO.input(PIN_SELECT) == GPIO.LOW:
        active.submit()
        time.sleep(0.5)
    else:
        pass
