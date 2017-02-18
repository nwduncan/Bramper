from __future__ import print_function
import subprocess
from subprocess import Popen, PIPE
import getAndSet


# this function will only work for shutter speed for now. this can easily
# be mopdified to adjust ISO as well, although this may not be necessary
def hdr(shot_num, stops):
    """
    shot_num ; number of shots (odd int only)
    stops ; stops (list: [2, 1, 0.67, 0.33]):
        the amount to adjust the exposure difference per shot (+/- shot_num-1/2)
    """
    ev = {0.33: 1,
          0.67: 2,
             1: 3,
             2: 6,
             3: 9,
             4: 12}
    cur_spd = getAndSet.shutterSpeedGet()
    speeds, choices = getAndSet.shutterDict()
    for k, v in speeds.items():
        if v == cur_spd:
            cur_opt = k
    print("{}: {}".format(cur_opt, cur_spd))

    ev_adjust = [ x*ev[stops] for x in range(1, (shot_num/2)+1) ]
    ev_adjust = [ x*-1 for x in ev_adjust[::-1] ] + [0] + ev_adjust
    print(ev_adjust)
    for adj in ev_adjust:
        print(speeds[cur_opt+adj]) 
