# exploratory camera controller program
# notes:
#   do not use sudo (seems to not change options, ignore settings etc)

import subprocess
from sys import exit

interval = raw_input("Enter the time between shots (in seconds):\n >> ")
frames = raw_input("Enter the number of frames to capture:\n >> ")

def takePics(interval, frames):
    if not interval.isdigit() or not frames.isdigit():
        print "Interval and Frames variables need to be integers.\n Exiting.."
        exit()
    else:
        to_call = ['gphoto2',
                   '--capture-image',
                   '--force-overwrite',
                   '--frames='+frames,
                   '--interval='+interval,
                   '--keep']
        subprocess.call(' '.join(to_call), shell=True)

try:
    takePics(interval, frames)
except subprocess.CalledProcessError as e:
    print e.output
