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

# find the index of an item in a list
def get_idx(item, options):
    for idx, opt in enumerate(options):
        if opt == item:
            return idx
        return

# incomplete -- use the get_refresh function to create these variables
options_shutter = camera_settings.get_shutter()
# idx_shutter = get_idx()
options_iso = camera_settings.get_iso_list()
options_aperture = camera_settings.get_aperture()

# get camera settings and display them
# this should also update the lists of options and the index of the current setting
def get_refresh(lcd):
    lcd.messages[shutter][1] = camera_settings.get_shutter()
    lcd.messages[iso][1] = camera_settings.get_iso()
    lcd.messages[aperture][1] = camera_settings.get_aperture()
    lcd.messages[misc][1] = ""
    lcd.refresh()

# set initial display
get_refresh(lcd)

# cursor movement
# 1 3
# 2 4
pos = 1
lcd.set_cursor_pos(1)

# control scheme 2
# reverse scroll through screen positions
def up():
    global pos
    pos-= 1 if pos > 1 else -3
    lcd.set_cursor_pos(pos)
    return

# forward scroll through screen positions
def down():
    global pos
    pos+= 1 if pos < 4 else -3
    lcd.set_cursor_pos(pos)
    return

# scroll right through current option values
def right():
    return

# scroll left through current option values
def left():
    return


# # control scheme 1
# def up():
#     global pos
#     pos-= 1 if pos%2 == 0 else 0
#     lcd.set_cursor_pos(pos)
#     return
#
# def down():
#     global pos
#     pos+= 1 if pos%2 == 1 else 0
#     lcd.set_cursor_pos(pos)
#     return
#
# def right():
#     global pos
#     pos+=2 if pos < 3 else 0
#     lcd.set_cursor_pos(pos)
#     return
#
# def left():
#     global pos
#     pos-=2 if pos > 2 else 0
#     lcd.set_cursor_pos(pos)
#     return
#
#
while True:
    move = raw_input('direction')
    locals()[move]()


# refreshes the LCD on a button press
# while True:
#     input_state = GPIO.input(button1_pin)
#     if input_state == False:
#         get_refresh(lcd)
#         time.sleep(0.2)
