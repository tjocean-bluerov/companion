#!/usr/bin/python

import os
from time import sleep
home = os.environ['HOME']

while True:
  while (os.system("ls /dev/snd/by-id 2>/dev/null")!=0):
    sleep(3)
  
  os.system(home+"/companion/scripts/start_audio.sh")
  sleep(2)

