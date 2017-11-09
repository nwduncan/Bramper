import interface
import camera_settings
import RPi.GPIO as GPIO
import time


## Initialise stuff
# button variables
button1_pin = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# These variables serve two purposes:
# - Calling gphoto2/camera specific config settings
# - To define where to display these elements in the interface.Display class
shutter = "shutterspeed2"
iso = "iso"
aperture = "f-number"
misc = "misc"

# initialise the LCD for use
#           LCD section:   1      2       3       4
lcd = interface.Display(shutter, iso, aperture, misc)

# find the index of an item in a list
def get_idx(item, options):
    for idx, opt in enumerate(options):
        if opt == item:
            return idx
    return False

# shutter
shutter_current = camera_settings.get_config(shutter)
shutter_options = camera_settings.get_options(shutter)
shutter_index = get_idx(shutter_current, shutter_options)

# iso
iso_current = camera_settings.get_config(iso)
iso_options = camera_settings.get_options(iso)
iso_index = get_idx(iso_current, iso_options)

# aperture
aperture_current = camera_settings.get_config(aperture)
aperture_options = camera_settings.get_options(aperture)
aperture_index = get_idx(aperture_current, aperture_options)


# get camera settings and display them
# this should also update the lists of options and the index of the current setting
def display_refresh(lcd):
    lcd.messages[shutter][1] = shutter_current
    lcd.messages[iso][1] = iso_current
    lcd.messages[aperture][1] = aperture_current
    lcd.messages[misc][1] = ""
    lcd.refresh()

# set initial display
display_refresh(lcd)



## Control scheme stuff
# cursor movement
# 0 2
# 1 3
pos = 0
lcd.set_cursor_pos(0)

# control scheme 2
# reverse scroll through screen positions
def up():
    global pos
    pos-= 1 if pos > 0 else -3
    lcd.set_cursor_pos(pos)
    return

# forward scroll through screen positions
def down():
    global pos
    pos+= 1 if pos < 3 else -3
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



## Interaction stuff
while True:
    move = raw_input('direction')
    locals()[move]()


# refreshes the LCD on a button press
# while True:
#     input_state = GPIO.input(button1_pin)
#     if input_state == False:
#         get_refresh(lcd)
#         time.sleep(0.2)
