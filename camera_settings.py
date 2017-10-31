import subprocess
from subprocess import Popen, PIPE


# set download location to be memory card
def set_target_card():
    # do not use sudo
    subprocess.call("gphoto2 --set-config-value /main/settings/capturetarget=1", shell=True)
    subprocess.call("gphoto2 --set-config capturetarget=\"Memory card\"", shell=True)


# return the current shutter speed
def get_shutter():
    child = Popen(["gphoto2", "--get-config=shutterspeed2"], stdout=PIPE)
    results = child.communicate()[0].split("\n")
    return results[2].split(" ")[1]


# return the current ISO setting
def get_iso():
    child = Popen(["gphoto2", "--get-config=iso"], stdout=PIPE)
    results = child.communicate()[0].split("\n")
    return results[2].split(" ")[1]

def get_aperture():
    child = Popen(["gphoto2", "--get-config=f-number"], stdout=PIPE)
    results = child.communicate()[0].split("\n")
    return results[2].split(" ")[1]


## debug & testing functions - remove ##

# return a dictionary of shutter speed options and a list which can be used
# for user input in selecting a shutter speed
def shutter_dict():
    raw_get = Popen(["gphoto2", "--get-config=shutterspeed2"], stdout=PIPE)
    raw_split = raw_get.communicate()[0].split("\n")
    speeds = { int(x.split()[1])+1: x.split()[2] for x in raw_split if "Choice:" in x }
    choices = sorted([ c for c in speeds ])
    return speeds, choices

# same as above but asked for input
def shutter_speed_options(display=True):
    raw_get = Popen(["gphoto2", "--get-config=shutterspeed2"], stdout=PIPE)
    raw_split = raw_get.communicate()[0].split("\n")
    speeds = { int(x.split()[1]): x.split()[2] for x in raw_split if "Choice:" in x }
    choices = sorted([ c for c in speeds ])
    for i in choices:
        print("Choice {}: {}".format(i, speeds[i]))
    while True:
        select = raw_input("Enter the desired shutter speed item number\n >> ")
        try:
            select = int(select)
            if select in choices:
                return speeds[select]
            continue
        except ValueError:
            continue

        # set the shutter speed
        def shutter_speed_set(shutter_speed=False):
            if not shutter_speed:
                shutter_speed = shutter_speed_options()
                to_call = 'gphoto2 --set-config shutterspeed2={}'.format(shutter_speed)
                subprocess.call(to_call, shell=True)
