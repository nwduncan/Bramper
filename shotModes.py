# Bulb ramping mode
# Investigate the point at which the shutter should be changed from a default
# shutter speed to bulb mode. ISO ramping also needs to be achievable.
class Bramp(object):
    def __init__(self, exln_start, exln_end, interval, bramp_length):
        self.exln_start = exln_start
        self.exln_end = exln_end
        # the interval variable should probably be part of a mode container class as it is not likely
        # to change throughout the timelapse
        self.interval = interval
        self.bramp_length = bramp_length
        self.shotObj = None
        self.buildShots()

    def buildShots(self):
        # make sure we're building a valid shot list
        if self.exln_end > self.interval:
            # this could be overcome with automatic ISO changes (a limit must be set though)
            raise ValueError("Maximum exposure time cannot exceed shot interval time.")
        # round total number of shots
        tot, rem = divmod(self.bramp_length, self.interval)
        frames = int(tot) if rem <= self.interval/2 else int(tot) + 1
        # increment to add to each shot
        ramp_int = (float(self.exln_end) - self.exln_start) / (frames - 1)
        # list of ramp intervals
        exposures = [self.exln_start] + [round(self.exln_start + (n * ramp_int), 2) for n in range(1, frames)]
        self.shotObj = exposures

    def returnShotObj(self):
        self.buildShots()
        return self.shotObj

    def __str__(self):
        # replace with something less shit
        return ' | '.join([ "Shot"+str(i+1)+": +"+str(self.interval*i)+"s @"+str(e)+"s" for i,e in enumerate(self.shotObj) ])



# Steady shot mode

# HDR mode - compatible with other modes?
# maybe a subset option of shutter mode steady shot?
