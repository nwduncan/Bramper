import interface
import camera_settings


# screen for viewing & changing camera exposure settings
class Settings(object):
    def __init__(self, shutter, iso, f_number, lcd):
        self.shutter = shutter
        self.iso = iso
        self.f_number = f_number
        self.other = "other"
        self.order = [self.shutter, self.iso, self.f_number, self.other]
        self.pos = 0
        self.editing = False
        self.lcd = lcd

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


    def set_active(self):
        self.refresh_camera_config() # check initialisation speed. might not be worth implementing
        self.refresh_display()
        self.edit_mode(False)
        self.pos = 0
        self.set_cursor_pos()


    # edit mode True/False
    def edit_mode(self, mode):
        self.editing = mode
        self.lcd.blink(mode)


    # refresh camera data
    def refresh_camera_config(self):
        for config in self.control:
            self.control[config][0] = camera_settings.get_config(config)
            self.control[config][1] = camera_settings.get_options(config)


    # refresh display
    def refresh_display(self):
        self.lcd.clear()
        original_pos = self.pos

        for idx, config in enumerate(self.layout):
            self.pos = idx
            self.set_cursor()
            self.lcd.message(self.layout[config][1])

        self.pos = original_pos
        self.set_cursor_pos()
        self.edit_mode(editing)


    # find where in list of options current setting is
    def get_idx(self, item, options):
        for idx, opt in enumerate(options):
            if opt == item:
                return idx

        return False


    # set the cursor position
    def set_cursor_pos(self):
        pos_setting = self.order[self.pos]
        self.lcd.set_cursor(self.layout[pos_setting][0][0], self.layout[pos_setting][0][1])


    ## All user input comes through the below methods
    ## The above methods are accessed from within the class only
    
    # reverse scroll through screen positions
    def up(self):
        if self.editing:
            self.pos-= 1 if self.pos > 0 else -3
            self.set_cursor_pos()


    # forward scroll through screen positions
    def down(self):
        if self.editing:
            self.pos+= 1 if self.pos < 3 else -3
            self.set_cursor_pos()


    # scroll right through current option values
    def right(self):
        if self.editing:
            current_config = self.order[self.pos]

            if self.control[current_config][2] is None:
                current = self.control[current_config][0]
            else:
                current = self.control[current_config][2]

            options = self.control[current_config][1]
            current_idx = self.get_idx(current, options)

            if current_idx < (len(options)-1):
                new_idx = current_idx+1
                new_setting = options[new_idx]
            else:
                new_idx = 0
                new_setting = options[new_idx]

            self.control[current_config][2] = new_setting
            self.layout[current_config][1] = new_setting
            self.refresh_display()


    # scroll left through current option values
    def left(self):
        if self.editing:
            current_config = self.order[self.pos]

            if self.control[current_config][2] is None:
                current = self.control[current_config][0]
            else:
                current = self.control[current_config][2]

            options = self.control[current_config][1]
            current_idx = self.get_idx(current, options)

            if current_idx > 0:
                new_idx = current_idx-1
                new_setting = options[new_idx]
            else:
                new_idx = len(options)-1
                new_setting = options[new_idx]

            self.control[current_config][2] = new_setting
            self.layout[current_config][1] = new_setting
            self.refresh_display()


    # apply settings
    def submit(self):
        for config in self.control:
            new_setting = self.control[config][2]
            if new_setting is not None:
                self.control[config][0] = new_setting
                camera_settings.set_config(config, new_setting)

        self.refresh_display()
        self.edit_mode(False)
