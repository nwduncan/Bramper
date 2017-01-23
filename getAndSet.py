from __future__ import print_function
import subprocess
from subprocess import Popen, PIPE

def shutterSpeedGet():
    child = Popen(["gphoto2", "--get-config=shutterspeed2"], stdout=PIPE)
    results = child.communicate()[0].split("\n")
    return results[2]

def shutterSpeedOptions(display=True):
    raw_get = Popen(["gphoto2", "--get-config=shutterspeed2"], stdout=PIPE)
    raw_split = raw_get.communicate()[0].split("\n")
    results = { int(x.split()[1]): x.split()[2] for x in raw_split if "Choice:" in x }
    choices = sorted([ c for c in results ])
    for i in choices:
        print("Choice {}: {}".format(i, results[i]))
    while True:
        select = raw_input("Enter the desired shutter speed item number\n >> ")
        try:
            select = int(select)
            if select in choices:
                print("allg")
                return results[select]
            print("naw1")
            continue
        except ValueError:
            print("naw2")
            continue

def shutterSpeedSet():
    shutter_speed = shutterSpeedOptions()
    to_call = 'gphoto2 --set-config shutterspeed2={}'.format(shutter_speed)
    subprocess.call(to_call, shell=True)
