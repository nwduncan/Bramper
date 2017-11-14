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
# - Has the potential to allow profiles for different cameras to be set up
shutter = "shutterspeed2"
iso = "iso"
aperture = "f-number"
misc = "misc"

# control = { 0: shutter,
#             1: iso,
#             2: aperture,
#             3: misc }

control = { 0: [shutter,
                  camera_settings.get_config(shutter),
                  camera_settings.get_options(shutter)]
              1: [iso,
                  camera_settings.get_config(iso),
                  camera_settings.get_options(iso)]
              2: [aperture,
                  camera_settings.get_config(shutter),
                  camera_settings.get_options(shutter)]
              3:  misc }


# initialise the LCD and set the default cursor position
lcd = interface.Display(control[0][1], control[1][1], control[2][1], control[3][1])
pos = 0
lcd.set_cursor_pos(0)

def display_refresh(lcd):
    lcd.messages[shutter][1] = shutter_current
    lcd.messages[iso][1] = iso_current
    lcd.messages[aperture][1] = aperture_current
    lcd.messages[misc][1] = ""
    lcd.refresh()

display_refresh(lcd)

# find the index of an item in a list
def get_idx(item, options):
    for idx, opt in enumerate(options):
        if opt == item:
            return idx
    return False

# # shutter
# shutter_current = camera_settings.get_config(shutter)
# shutter_options = camera_settings.get_options(shutter)
# shutter_index = get_idx(shutter_current, shutter_options)
#
# # iso
# iso_current = camera_settings.get_config(iso)
# iso_options = camera_settings.get_options(iso)
# iso_index = get_idx(iso_current, iso_options)
#
# # aperture
# aperture_current = camera_settings.get_config(aperture)
# aperture_options = camera_settings.get_options(aperture)
# aperture_index = get_idx(aperture_current, aperture_options)



# set initial display
display_refresh(lcd)



## Control scheme stuff
# cursor movement
# 0 2
# 1 3



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
