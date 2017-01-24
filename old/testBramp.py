import subprocess
import time

# change in bulb / number of shots - 1

def bramp(start_B, end_B, interval, length):

    # build shot details
    # round number of shots to closest whole frame
    tot, rem = divmod(length, interval)
    if rem == 0 or rem < interval/2:
        frames = int(tot)
        # frames = range(0, int(tot))
    else:
        frames = int(tot) + 1
        # frames = range(0, int(tot)+1)
    # ramp interval
    ramp_int = (float(end_B) - start_B) / (frames - 1)
    # list of ramp intervals
    exposures = [start_B] + [round(start_B + (n * ramp_int),2) for n in range(1, frames)]
    # combined the two lists to create a [count-1, exposure time] pair
    # shot_details = zip(frames, exposures)

    # take the pictures
    for shot_num, exp in enumerate(exposures):
        print "Taking image {} with {}s exposure time...".format(shot_num+1, exp)
        gp = "gphoto2 --capture-image --bulb={}".format(exp)
        subprocess.call(gp, shell=True)
        time.sleep(interval)



start_B = float(raw_input("Bulb start exposure time:\n>>"))
print "\n"
end_B = float(raw_input("Bulb end exposure time:\n>>"))
print "\n"
interval = float(raw_input("Time between exposures:\n>>"))
print "\n"
shots = float(raw_input("Length of time lapse:\n>>"))
print "\nRunning bramp..\n"
bramp(start_B, end_B, interval, shots)
