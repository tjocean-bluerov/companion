#!/usr/bin/python

import os
from time import sleep 

while True:
  while ((os.system("ls /dev/ACM* 2>/dev/null") == 0) or (os.path.isfile("/home/pi/companion/scripts/start_mavproxy_telem_splitter.sh")==0)):
    sleep(2)

  os.system("/home/pi/companion/scripts/start_mavproxy_telem_splitter.sh")
  sleep(2)

