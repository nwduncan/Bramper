import interface
import camera_settings
import Adafruit_CharLCD as LCD

#### replace all references to interface.py with direct adafruitLCD communication. ####

# screen for viewing & changing camera exposure settings
class Settings(object):
    def __init__(self, shutter, iso, f_number):
        self.shutter = shutter
        self.iso = iso
        self.f_number = f_number
        self.other = "other"
        self.order = [self.shutter, self.iso, self.f_number]
        self.control = {
            shutter: [camera_settings.get_config(shutter),          # [current shutter
                      camera_settings.get_options(shutter), None],  #  shutter options, temp/next setting]
                iso: [camera_settings.get_config(iso),              # [current iso
                      camera_settings.get_options(iso), None],      #  iso options, temp/next setting]
           f_number: [camera_settings.get_config(f_number),         # [f_number speed
                      camera_settings.get_options(f_number), None]} #  f_number options, temp/next setting]
        self.layout = { self.shutter:  [[0,0], ""],
                        self.iso:      [[0,1], ""],
                        self.f_number: [[8,0], ""],
                        self.other:    [[8,1], ""] }
        self.lcd = interface.LCD(order[0], order[1], order[2], order[3])
        self.pos = 0
        self.lcd.set_cursor_pos(0)
        self.editing = False

        self.refresh_display()

    # edit mode True/False
    def edit_mode(self, mode):
        self.editing = mode
        self.lcd.blink(mode) #replace with direct communication to Adafruit module?

        return

    # refresh camera data
    def refresh_camera_config(self):
        for config in self.control:
            self.control[config][0] = camera_settings.get_config(config)
            self.control[config][1] = camera_settings.get_options(config)

        return

    # refresh display
    def refresh_display(self):
        lcd.clear() # replace with direct call to module

        for config in self.control:
            self.lcd.set_message(config, self.control[config][0])

        self.lcd.set_cursor_pos(self.pos)
        self.edit_mode(editing)

        return

    # find the index of an item in a list
    # used to turn pos variable in to config name
    def get_idx(self, item, options):
        for idx, opt in enumerate(options):
            if opt == item:
                return idx

        return False

    # reverse scroll through screen positions
    def up(self):
        if self.editing:
            self.pos-= 1 if self.pos > 0 else -3
            self.lcd.set_cursor_pos(self.pos)

        return

    # forward scroll through screen positions
    def down(self):
        if self.editing:
            self.pos+= 1 if self.pos < 3 else -3
            self.lcd.set_cursor_pos(self.pos)

        return

    # scroll right through current option values
    def right(self):
        if self.editing:
            current_name = self.order[self.pos]

            if self.control[current_name][2] is None:
                current = self.control[current_name][0]
            else:
                current = self.control[current_name][2]

            options = self.control[current_name][1]
            current_idx = self.get_idx(current, options)

            if current_idx < (len(options)-1):
                new_idx = current_idx+1
                new_config = options[new_idx]
            else:
                new_idx = 0
                new_config = options[new_idx]

            self.control[current_name][2] = new_config
            self.lcd.set_message(current_name, new_config)
            self.lcd.set_cursor_pos(self.pos)

        return

    # scroll left through current option values
    def left(self):
        if self.editing:
            current_name = self.order[self.pos]

            if self.control[current_name][2] is None:
                current = self.control[current_name][0]
            else:
                current = self.control[current_name][2]

            options = self.control[current_name][1]
            current_idx = self.get_idx(current, options)

            if current_idx > 0:
                new_idx = current_idx-1
                new_config = options[new_idx]
            else:
                new_idx = len(options)-1
                new_config = options[new_idx]

            self.control[current_name][2] = new_config
            self.lcd.set_message(current_name, new_config)
            self.lcd.set_cursor_pos(self.pos)

        return

    # apply settings
    def submit(self):
        for config in self.control:
            new_setting = self.control[config][2]
            if new_setting is not None:
                self.control[config][0] = new_setting
                camera_settings.set_config(config, new_setting)

        self.refresh_display()
        self.edit_mode(False)

        self.lcd.blink(False)
