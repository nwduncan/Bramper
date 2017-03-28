# this is currently working but proves to be too slow for one off shots.
# can be used in conjunction with the timelapse module to create hdr timelapses

from __future__ import print_function
import subprocess
from subprocess import Popen, PIPE
import cameraSettings

shutter_speeds, choices = cameraSettings.shutterDict()

# this function will currently only work with shutter speed. this can easily
# be mopdified to adjust ISO as well, although this may not be necessary
def hdr(shot_num, stops):
    """
    shot_num ; number of shots (odd int only)
    stops ; stops (list: [2, 1, 0.67, 0.33]):
        the amount to adjust the exposure difference per shot
    """
    ev = {0.33: 1,
          0.67: 2,
             1: 3,
             2: 6,
             3: 9,
             4: 12}

    cur_spd = cameraSettings.shutterSpeedGet()
    for k, v in shutter_speeds.items():
        if v == cur_spd:
            cur_opt = k

    ev_adjust = [ x*ev[stops] for x in range(1, (shot_num/2)+1) ]
    ev_adjust = [ x*-1 for x in ev_adjust[::-1] ] + [0] + ev_adjust

    for ev in ev_adjust:
        set_speed = shutter_speeds[cur_opt+ev]
        print(set_speed)
        cameraSettings.shutterSpeedSet(set_speed)
        subprocess.call('gphoto2 --capture-image', shell=True)

    cameraSettings.shutterSpeedSet(cur_spd)
