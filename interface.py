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
# 0000000022222222
# 1111111133333333
# QUAD_POS = { 0: [0,0],
#              1: [0,1],
#              2: [8,0],
#              3: [8,1] }


# LCD display control class
class Interface(object):
    def __init__(self, quad0, quad1, quad2, quad3):
        self.lcd = LCD.Adafruit_CharLCD(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6,
                                        LCD_D7, LCD_COL, LCD_ROWS, LCD_BL)
        self.screens = []
        # self.messages = { quad0: [QUAD_POS[0], ""],
        #                   quad1: [QUAD_POS[1], ""],
        #                   quad2: [QUAD_POS[2], ""],
        #                   quad3: [QUAD_POS[3], ""] }

    def add(self, name, layout):
        new_screen = { name: layout }
        self.screens.append(new_screen)

    def refresh(self):
        self.lcd.clear()
        for msg in self.messages:
            self.lcd.set_cursor(self.messages[msg][0][0], self.messages[msg][0][1])
            self.lcd.message(self.messages[msg][1])

    def set_message(self, screen, section, message):
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

    def blink(self, mode):
        self.lcd.blink(mode)

    def clear(self):
        self.lcd.clear()
