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
        self.shotObj = None
        self.buildShotObj()

    def buildShotObj(self):

        # determine total frame count
        tot, rem = divmod(self.bramp_length, self.interval)
        frames = int(tot) if rem <= self.interval/2 else int(tot) + 1

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
        ramp_int = (float(end_exposure) - start_exposure) / (frames - 1)

        # list of ramp intervals
        # [shot number, elapsed time, exposure length (adjusted)]
        exposures = [[1, 0, start_exposure]]
        cur_exposure = start_exposure + ramp_int

        # build the shot details
        for n in range(1, frames):

            # if the current exposure length is less than 1 second use the camera's preset shutter speed options
            if cur_exposure < 1:
                # find the closest preset shutter speed to the current exposure time
                str_exposure = min(self.cam_shutter_dict.items(), key=lambda (_, v): abs(v - cur_exposure))[0]
                # diff = cur_exposure - float(Fraction(str_exposure))
                exposures.append([n, n*self.interval, str_exposure])
                cur_exposure+=ramp_int

            # if the current exposure is greater than 1 second use bulb mode
            else:
                exposures.append([n, n*self.interval, cur_exposure, round(cur_exposure, 1)])
                cur_exposure+=ramp_int

        self.shotObj = exposures

    def shotObj(self):
        self.buildShotObj()
        return self.shotObj

    def __str__(self):
        # replace with something less shit
        # return ' | '.join([ "Shot"+str(i+1)+": +"+str(self.interval*i)+"s @"+str(e)+"s" for i,e in enumerate(self.shotObj) ])
        return self.shotObj



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
        delf.shotObj = None

    def buildShotObj(self):
        pass
