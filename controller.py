import interface
import camera_settings
import RPi.GPIO as GPIO
import time

# button variables
button1_pin = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LCD variables
shutter = "shutter"
iso = "iso"
aperture = "aperture"
misc = "misc"
lcd = interface.Display(shutter, iso, aperture, misc)

# get camera settings (currenlty shutter only)
def get_refresh(lcd):
    lcd.messages[shutter][1] = camera_settings.shutterSpeedGet()
    lcd.messages[iso][1] = "800"
    lcd.messages[aperture][1] = "f1.4"
    lcd.messages[misc][1] = ""
    lcd.refresh()

# refreshes the LCD on a button press
while True:
    input_state = GPIO.input(button1_pin)
    if input_state == False:
        get_refresh(lcd)
        time.sleep(0.2)
