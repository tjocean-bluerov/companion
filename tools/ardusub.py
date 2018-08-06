#!/usr/bin/python

from pymavlink import mavutil
import time
import sys

#Establish connection with pixhawk
master = mavutil.mavlink_connection('udpout:localhost:9000')

for x in range(3):
	#Send request for autopilot version
	master.mav.autopilot_version_request_send(
		master.target_system,
		master.target_component
	)
	msg = master.recv_match(type='AUTOPILOT_VERSION')

	#Check if version information was obtained
	#Print version
	if msg:
		version_d = msg.to_dict()
		version_hex = hex(version_d["flight_sw_version"])
		print ('.'.join(version for version in version_hex[2:-2:2]))
		sys.exit(0)

	time.sleep(1)

#Exit the script with an error code after 3 attempts

print ("Error!")
sys.exit(1)
