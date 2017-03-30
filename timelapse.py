from __future__ import print_function
import subprocess
#from subprocess import Popen, PIPE
import cameraSettings
from fractions import Fraction
from threading import Timer

# Bulb ramping mode
class Bramp(object):
    # modify to allow either an interval length or x number of shots
    def __init__(self, exln_start, exln_end, interval, bramp_length):

        self.exln_start = str(exln_start)
        self.exln_end = str(exln_end)
        self.interval = interval
        self.bramp_length = bramp_length

        # create dictionary of shutter speed settings to use for when the bulb exposure is too short
        # currently this is anything less than 1 second
        self.cam_shutter_dict = cameraSettings.shutterDict()[0]
        self.cam_shutter_dict = { v: float(Fraction(v)) for k, v in self.cam_shutter_dict.iteritems() if float(Fraction(v)) < 1 }
        self.cam_shutter_dict['1'] = 1

        # instance variables to compute
        self.shot_details = None
        self.frames = None

        # build shot details
        self.buildShotDetails()


    def buildShotDetails(self):

        # determine total frame count
        tot, rem = divmod(self.bramp_length, self.interval)
        self.frames = int(tot) if rem <= self.interval/2 else int(tot) + 1

        # set start and end exposure variables to guide ramp interval
        # end exposure
        if self.exln_end in self.cam_shutter_dict:
            end_exposure = self.cam_shutter_dict[self.exln_end]
        else:
            end_exposure = int(self.exln_end)
        # start exposure
        if self.exln_start in self.cam_shutter_dict:
            start_exposure = self.cam_shutter_dict[self.exln_start]
        else:
            start_exposure = int(self.exln_start)

        # ramping interval
        ramp_int = (float(end_exposure) - start_exposure) / (self.frames - 1)

        # build the shot details
        # { 0: [ 'preset', '1/4000' ],  # for preset shutter speed exposures
        #   1: [ 'bulb', 15.2 ] }       # for bulb exposures
        shot_dict = {}
        cur_exposure = start_exposure

        for i in range(0, self.frames):
            # if the current exposure length is less than 1 second use the camera's preset shutter speed options
            if cur_exposure < 1:
                # find the closest preset shutter speed to the current exposure time
                str_exposure = min(self.cam_shutter_dict.items(), key=lambda (_, v): abs(v - cur_exposure))[0]
                # diff = cur_exposure - float(Fraction(str_exposure))
                shot_dict[i] = ['preset', str_exposure]
                cur_exposure+=ramp_int
            # if the current exposure is greater than 1 second use bulb mode
            else:
                shot_dict[i] = ['bulb', round(cur_exposure, 1)]
                cur_exposure+=ramp_int

        self.shot_details = shot_dict


    def captureImage(self, seq_num):

        shot_settings = self.shot_details[seq_num]

        if shot_settings[0] == 'preset':
            shutter_speed = shot_settings[1]
            # change shutter speed
            cameraSettings.shutterSpeedSet(shutter_speed)
            # capture image
            sub_p = 'gphoto2 --capture-image'
            subprocess.call(sub_p, shell=True)

        else:
            shutter_speed = shot_settings[1]
            # capture image
            sub_p = 'gphoto2 --capture-image --bulb='+str(shutter_speed)
            subprocess.call(sub_p, shell=True)


    def __str__(self):
        # replace with something less shit
        # return ' | '.join([ "Shot"+str(i+1)+": +"+str(self.interval*i)+"s @"+str(e)+"s" for i,e in enumerate(self.shot_list) ])
        return self.shot_list



# timelapse management class
class Timelapse(object):

    def __int__(self):
        self.session_full = []
        self.session = None
        self.session_idx = 0
        self.seq_idx = 0
        self.current_interval = None
        self.timer = None
        self.running = False

    # establish/modify the timelapse order sequence
    def add(self, tl_object, order=False):
        if not order:
            self.session_full.append(tl_object)
        else:
            self.session_full.insert(order, tl_object)

    # method for defining when to begin the timelapse
    # options should include:
    #   - starting at the start/end/seq_num of a section - this will alow a bulb ramp to be
    #   concluded/begun at a specific time (sunrise, sunset, moon rise etc)
    #   - instantly (button press, user input)
    def defineStart(self):
        pass

    # a once off method for beginning the timelapse
    # this will call the first shot and then begin the automated capture sequence
    def start(self):
        self.session = self.session_full[self.session_idx]
        self.current_interval = self.session.interval
        self.timekeeper()
        self.session.captureImage(self.seq_idx)
        self.seq_idx+=1

    def timekeeper(self):
        if not self.running:
            self.timer = Timer(self.current_interval, self.capture)
            self.timer.start()
            self.running = True

    def capture(self):
        self.running = False
        self.timekeeper()
        # capture
        # continue to next shot
        session_len = len(self.session.shot_details)
        if self.seq_idx < session_len:
            self.session.captureImage(self.seq_idx)
            self.seq_idx+=1

        # finished the current session
        number_of_sessions = len(self.session_full)
        elif self.session_idx < number_of_sessions:
                self.session_idx+=1
                self.session = self.session_full[self.session_idx]
                self.seq_idx = 0
                self.current_interval = self.session.interval

        # finished timelapse
        else:
            # clean up
            stop()

    # stop taking images
    def stop(self):
        self.timer.cancel()

    # get current status of timelapse
    def status(self):
        pass
