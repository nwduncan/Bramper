from threading import Timer
import RPi.GPIO as GPIO
import time



# timelapse display and control
class Timelapse(object):


    def __init__(self, lcd, bulb, interval, number):

        self.lcd = lcd
        # length of time (s) shutter is to be open
        self.bulb = bulb
        # length of time (s) between shutter opening. this value needs to be > than bulb value
        self.interval = interval
        self.interval_count = 0
        # number of shots to take in total
        self.number = number
        self.number_count = 0

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
        self.refresh_display()


    # # set screen as active
    # def set_active(self):
    #     self.active = True
    #     self.refresh_display()


    # refresh the lcd display
    def refresh_display(self):
        self.lcd.clear()
        # shot count
        self.lcd.set_cursor(0, 0)
        start_text = "Shots:"
        end_text = "{}/{}".format(self.number_count, self.number)
        self.lcd.message(self.pad(start_text, end_text))
        # count down (bulb/timer)
        self.lcd.set_cursor(0, 1)
        start_text = "Bulb:" if self.shooting else "Next shot:"
        end_text =  str(self.interval-self.interval_count-self.bulb) if self.shooting else str(self.interval-self.interval_count)
        self.lcd.message(self.pad(start_text, end_text))
            # self.lcd.message("{}".format(self.interval-self.interval_count if self.timer is not None else ""))
            # time remaining
            # self.lcd.set_cursor(0, 2)
            # self.lcd.message("{}".format(self.interval-self.interval_count if self.timer is not None else ""))
            # # progress bar
            # self.lcd.set_cursor(0, 3)
            # self.lcd.message("{}".format(self.interval-self.interval_count if self.timer is not None else ""))



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

        self.refresh_display()


    # take shot
    def capture(self):
        if self.number_count < self.number:
            self.shutter_release(self.bulb)
            self.number_count += 1
            self.interval_count = 0

            # finished timelapse
            if self.number_count == self.number:
                self.stop()


    def shutter_release(self, length):
        if not self.shooting:
            self.bulb_timer = Timer(length, self.shutter_close)
            GPIO.output(self.release_pin, GPIO.HIGH)
            self.bulb_timer.start()
            self.shooting = True

    def shutter_close(self):
        GPIO.output(self.release_pin, GPIO.LOW)
        self.shooting = False


    # stop taking images
    def stop(self):
        self.timer.cancel()
        print "--- {} seconds ---".format(time.time() - self.start_time)


    def pad(self, start_text, end_text):
        total_length = len(start_text) + len(end_text)
        if total_length <= 20:
            return start_text+" "*(20-total_length)+end_text
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
