#!/bin/sh
# startup.sh
# navigate to the home dir, then to this dir, run startup python script, then navigate back to the home dir

pushd /home/pi/Desktop/Bramper
sudo python startup.py
popd
