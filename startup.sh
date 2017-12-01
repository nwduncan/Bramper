#!/bin/sh
# startup.sh
# navigate to the home dir, then to this dir, run startup python script, then navigate back to the home dir

cd /
cd home/pi/Desktop/Pi-Lapse
sudo python startup.py
cd /
