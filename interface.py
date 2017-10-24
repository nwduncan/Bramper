import Adafruit_CharLCD as LCD
import cameraSettings
import time

# wiring variables
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22

# lcd variables
lcd_backlight = 4
lcd_columns = 16
lcd_rows = 2

# variables to define LCD message quadrants
# format (column and row start @ 0):
# 1111111133333333
# 2222222244444444


# LCD control class
class display(object):

    def __init__(self):
        self.lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
        self.messages = { "shutter":  [[0,0], ""],
                          "iso":      [[0,1], ""],
                          "aperture": [[8,0], ""],
                          "misc":     [[8,1], ""] }

    def refresh(self):
        self.lcd.clear()
        for msg in self.messages:
            self.lcd.set_cursor(self.messages[msg][0][0], self.messages[msg][0][1])
            self.lcd.message(self.messages[msg][1])

    def set_message(self, section, message):
        if section in self.messages:
            self.messages[section][1] = message
            self.refresh()

        else:
            self.lcd.home()
            self.lcd.message("Invalid section")
            self.lcd.set_cursor(0,1)
            self.lcd.message("Returning...")
            time.sleep(3)
            self.refresh()














#
