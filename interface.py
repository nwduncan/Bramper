# a basic LCD handler for displaying camera info

import Adafruit_CharLCD as LCD
import time

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

# dictionary to define LCD message quadrants
# column and row start @ 0
# 1111111133333333
# 2222222244444444
QUAD_POS = { 1: [0,0],
             2: [0,1],
             3: [8,0],
             4: [8,1] }


# LCD display control class
class Display(object):
    def __init__(self, quad1, quad2, quad3, quad4):
        self.lcd = LCD.Adafruit_CharLCD(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7, LCD_COL, LCD_ROWS, LCD_BL)
        self.messages = { quad1: [QUAD_POS[1], ""],
                          quad2: [QUAD_POS[2], ""],
                          quad3: [QUAD_POS[3], ""],
                          quad4: [QUAD_POS[4], ""] }

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

    def set_cursor_pos(self, position):
        self.lcd.set_cursor(QUAD_POS[position][0], QUAD_POS[position][1])
        self.lcd.blink(True)













#
