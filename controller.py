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
# - Currently 'info' represents the section which will display control options (enter, cancel, refresh, etc)
shutter = "shutterspeed2"
iso = "iso"
aperture = "f-number"
info = "info"
order = [shutter, iso, aperture, info]

# control = { config_name: [current_setting, options, new_setting] }
control = { shutter: [camera_settings.get_config(shutter), camera_settings.get_options(shutter), None],
            iso: [camera_settings.get_config(iso), camera_settings.get_options(iso), None],
            aperture: [camera_settings.get_config(aperture), camera_settings.get_options(aperture), None]}

# initialise the LCD and set the default cursor position
lcd = interface.Display(order[0], order[1], order[2], order[3])
pos = 0
lcd.set_cursor_pos(0)

editing = False

def edit_mode(mode):
    global editing, lcd
    editing = mode
    lcd.blink(mode)

    return

# refresh camera data
def refresh_camera_config():
    global control

    for config in control:
        control[config][0] = camera_settings.get_config(config)
        control[config][1] = camera_settings.get_options(config)

    return

# refresh display
def refresh_display():
    global lcd, control, editing

    lcd.clear()

    for config in control:
        lcd.set_message(config, control[config][0])

    lcd.set_cursor_pos(pos)
    edit_mode(editing)

    return

refresh_display()



# find the index of an item in a list
# used to turn pos variable in to config name
def get_idx(item, options):
    for idx, opt in enumerate(options):
        if opt == item:
            return idx

    return False


# control scheme 2
# reverse scroll through screen positions
def up():
    global editing
    if editing:

        global pos
        pos-= 1 if pos > 0 else -3
        lcd.set_cursor_pos(pos)

    return

# forward scroll through screen positions
def down():
    global editing
    if editing:

        global pos
        pos+= 1 if pos < 3 else -3
        lcd.set_cursor_pos(pos)

    return

# scroll right through current option values
def right():
    global editing
    if editing:

        global pos, order, lcd, control

        current_name = order[pos]

        if control[current_name][2] is None:
            current = control[current_name][0]
        else:
            current = control[current_name][2]

        options = control[current_name][1]
        current_idx = get_idx(current, options)

        if current_idx < (len(options)-1):
            new_idx = current_idx+1
            new_config = options[new_idx]
        else:
            new_idx = 0
            new_config = options[new_idx]

        control[current_name][2] = new_config
        lcd.set_message(current_name, new_config)
        lcd.set_cursor_pos(pos)

    return

# scroll left through current option values
def left():
    global editing
    if editing:

        global pos, order, lcd, control

        current_name = order[pos]

        if control[current_name][2] is None:
            current = control[current_name][0]
        else:
            current = control[current_name][2]

        options = control[current_name][1]
        current_idx = get_idx(current, options)

        if current_idx > 0:
            new_idx = current_idx-1
            new_config = options[new_idx]
        else:
            new_idx = len(options)-1
            new_config = options[new_idx]

        control[current_name][2] = new_config
        lcd.set_message(current_name, new_config)
        lcd.set_cursor_pos(pos)

    return

# apply settings
def submit():
    global control, lcd

    for config in control:
        new_setting = control[config][2]
        if new_setting is not None:
            control[config][0] = new_setting
            camera_settings.set_config(config, new_setting)

    refresh_display()
    edit_mode(False)

    lcd.blink(False)

# testing only. remove once command line function calling isn't required
def edit():
    global editing
    editing = not editing
    edit_mode(editing)

    return


# allows functions to be called from command line while testing
while True:
    function = raw_input('function')
    locals()[function]()


# refreshes the LCD on a button press
# while True:
#     input_state = GPIO.input(button1_pin)
#     if input_state == False:
#         get_refresh(lcd)
#         time.sleep(0.2)
