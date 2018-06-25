#!/usr/bin/python

import os
from time import sleep 
import sys
home = os.environ['HOME']

os.system("sudo modprobe bcm2835-v4l2")

while True:
  while (os.system("ls /dev/video* 2>/dev/null") != 0) or (os.path.isfile(home + "/companion/start_video.sh")):
    sleep(5)
  if len(sys.argv) == 1:
    os.system(home + "/companion/scripts/start_video.sh $(cat /home/pi/vidformat.param)")
  else:
    os.system(home + "/companion/scripts/start_video.sh " + sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3] + " " + sys.argv[4])
  sleep(2)


