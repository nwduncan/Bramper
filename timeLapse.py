from __future__ import print_function
import subprocess
#from subprocess import Popen, PIPE
import cameraSettings
from fractions import Fraction

# Bulb ramping mode
# Investigate the point at which the shutter should be changed from a default
# shutter speed to bulb mode. ISO ramping also needs to be achievable.
class Bramp(object):

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

        self.shot_details = exposures


    def captureImage(self, seq_num):

        shot_settings = self.shot_list[seq_num]

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


# here be unused classes

# Session class for combining different timelapse objects
# this will be called when a timelapse commences
class Session(object):
    def __init__(self):
        self.session = []

    def add(self, mode):
        pass


# a parent class for the different time lapse modes
class Segment(object):
    def __init__(self, mode):
        self.mode = mode


# Steady shot mode
class Steady(object):
    def __init__(self, shot_mode, exp_len, interval, n_shots):
        self.shot_mode = shot_mode
        self.exp_len = exp_len
        self.interval = interval
        self.n_shots = n_shots
        delf.shotList = None

    def buildShotList(self):
        pass
