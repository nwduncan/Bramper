from threading import Timer
import RPi.GPIO as GPIO
import time
import Adafruit_CharLCD as LCD

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

# timelapse display and control
class Timelapse(object):


    def __init__(self, bulb, interval, number):

        # length of time (s) shutter is to be open
        self.bulb = bulb
        # length of time (s) between shutter opening. this value needs to be > than bulb value
        self.interval = interval
        self.interval_count = 0
        # number of shots to take in total
        self.number = number
        self.number_count = 0

        self.lcd = LCD.Adafruit_CharLCD(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7, LCD_COL, LCD_ROWS, LCD_BL)
        self.lcd.clear()

        # timers
        self.timer = None # intervalometer
        self.bulb_timer = None # bulb
        # timer statuses
        self.running = False # intervalometer status
        self.shooting = False # bulb status

        # used to compare perfect runtime vs actual runtime
        self.start_time = None

        # RPi GPIO settings
        self.release_pin = 19
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.release_pin, GPIO.OUT)


    # a once off method for beginning the timelapse
    # this will call the first shot and then begin the automated capture sequence
    def start(self):
        print "Started timelapse. Results should take {} seconds".format((self.number-1)*self.interval)
        self.intervalometer()
        self.capture()
        self.refresh_top()


    # # set screen as active
    # def set_active(self):
    #     self.active = True
    #     self.refresh_top()


    # refresh the lcd display
    def refresh_top(self):
        # self.lcd.clear()
        # shot count & countdown
        self.lcd.set_cursor(0, 0)
        start_text = "{}/{}".format(self.number_count, self.number)
        end_text = str(self.interval-(self.interval-self.bulb)-self.interval_count) if self.shooting else str(self.interval-self.interval_count)
        self.lcd.message(self.pad(start_text, end_text))
        print start_text
        print end_text

    def refresh_bottom(self):
        self.lcd.set_cursor(0, 1)
        if self.shooting:
            self.lcd.message(chr(255)*16)
        else:
            if self.number_count < self.number:
                self.lcd.message('-'*16)
            else:
                self.lcd.message('    complete    ')
                self.refresh_top()

    # use threading to keep intervals somewhat correct
    def intervalometer(self):
        if not self.running:
            self.timer = Timer(1, self.update)
            self.timer.start()
            self.running = True


    # determine whether to take image or just refresh display
    def update(self):
        self.running = False
        self.intervalometer()
        self.interval_count += 1

        if self.interval_count == self.interval:
            self.capture()

        self.refresh_top()


    # take shot
    def capture(self):
        if self.number_count < self.number:
            self.shutter_release(self.bulb)
            self.number_count += 1
            self.interval_count = 0


    def shutter_release(self, length):
        if not self.shooting:
            self.bulb_timer = Timer(length, self.shutter_close)
            GPIO.output(self.release_pin, GPIO.HIGH)
            self.bulb_timer.start()
            self.shooting = True
            self.refresh_bottom()
            print "shot"


    def shutter_close(self):
        GPIO.output(self.release_pin, GPIO.LOW)
        self.shooting = False
        self.refresh_bottom()
        if self.number_count == self.number:
            self.stop()


    # stop taking images
    def stop(self):
        self.timer.cancel()
        # print "--- {} seconds ---".format(time.time() - self.start_time)


    def pad(self, start_text, end_text):
        total_length = len(start_text) + len(end_text)
        if total_length <= 16:
            return start_text+" "*(16-total_length)+end_text
        else:
            return "string too long" # replace with a useable solution



# ####################
# Shutter:      1/4000
# F-number:      f/2.8
# ISO            12800
# --------------------
# Shots:      521/1000
# Next shot:        60      Bulb:        12
# Time left:  10:23:42
######################
