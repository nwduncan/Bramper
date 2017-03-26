import subprocess, time

time.sleep(10)
subprocess.call("sudo killall gvfs-gphoto2-volume-monitor", shell=True)
