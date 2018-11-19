#!/usr/bin/python

import platform
import csv
import time
import os
from pymavlink import mavutil
from pymavlink.dialects.v10 import common as mavlink
from pymavlink import mavparm
from optparse import OptionParser
home = os.environ['HOME']
timeout = 1

parser = OptionParser()
parser.add_option("--file", dest="file", default=None, help="Load from file")
(options,args) = parser.parse_args()

if options.file is not None:
    try:
        print("Attempting upload from file %s") % options.file
        filename = options.file
    except Exception as e:
        print("Error opening file %s: %s") % (options.file, e)
        exit(1)
else:
    filename = 'standard.params'

# Stop screen session with mavproxy
print("Stopping mavproxy")
os.system("screen -X -S mavproxy quit")

# Port settings
port = ''
if platform.system() == 'Linux':
    port = '/dev/serial/by-id/usb-3D_Robotics_PX4_FMU_v2.x_0-if00'
elif platform.system() == 'Darwin':
    port = '/dev/tty.usbmodem1'


if not os.path.exists(port):
    raise Exception("port does not exist: %s" % port)

master = mavutil.mavlink_connection(port)
master.wait_heartbeat()

# Reset parameters to firmware defaults
print("Resetting parameters to defaults."),

master.mav.command_long_send(
    1, # target system
    1, # target component
    mavutil.mavlink.MAV_CMD_PREFLIGHT_STORAGE, # command
    0, # confirmation
    2, # erase
    0,0,0,0,0,0) # unused params

verified = False
start = time.time()
while time.time() < start + timeout:
    msg = master.recv_match()
    if msg is not None:
        if msg.get_type() == "COMMAND_ACK" and msg.command == mavutil.mavlink.MAV_CMD_PREFLIGHT_STORAGE and msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
            print(" OK")
            verified = True
            break
    time.sleep(0.01)

if not verified:
    print(" FAIL!")
    exit(1)

print("Rebooting."),

master.mav.command_long_send(
    1, # target system
    1, # target component
    mavutil.mavlink.MAV_CMD_PREFLIGHT_REBOOT_SHUTDOWN, # command
    0, # confirmation
    1, # reboot
    0,0,0,0,0,0) # unused params

verified = False
start = time.time()
while time.time() < start + timeout:
    msg = master.recv_match()
    if msg is not None:
        if msg.get_type() == "COMMAND_ACK" and msg.command == mavutil.mavlink.MAV_CMD_PREFLIGHT_REBOOT_SHUTDOWN and msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
            print(" OK")
            verified = True
            break
    time.sleep(0.01)

if not verified:
    print(" FAIL!")
    exit(1)

master.close()

print("waiting for %s to drop..." % port)
while not os.system("ls " + port + " > /dev/null 2>&1"):
    time.sleep(0.1)
    
print("waiting for connection to %s..." % port)
while os.system("ls " + port + " > /dev/null 2>&1"):
    time.sleep(0.1)

print("Waiting for heartbeat.")

try:
    master = mavutil.mavlink_connection(port)
    master.wait_heartbeat()
except:
    print("Trying again.")
    time.sleep(6)
    master = mavutil.mavlink_connection(port)
    master.wait_heartbeat()

# Upload parameter file
print("Uploading parameter file.")

failed = []

with open(filename,'r') as f:
    for line in f:
        line = line.split(',')
        name = line[0]
        value = float(line[1])
        
        verified = False
        attempts = 0
        
        print("Sending " + name + " = " + str(value) + "\t\t\t"),
        
        while not verified and attempts < 3:
            master.param_set_send(name,value)
            start = time.time()
                        
            while time.time() < start + timeout:
                msg = master.recv_match()
                if msg is not None:
                    if msg.get_type() == "PARAM_VALUE" and msg.param_id == name and msg.param_value == value:
                        print(" OK")
                        verified = True
                        break
                time.sleep(0.01)
                
            attempts = attempts + 1
            
        if not verified:
            print(" FAIL!")
            failed.append(name)

    f.close()
    if len(failed) > 0:
        print("Failed to set %s") % failed
    else:
        print("Parameter flash successful!")

# Wait a few seconds
print("Waiting to restart mavproxy...")
time.sleep(4)

# Start screen session with mavproxy
print("Restarting mavproxy")
os.system("screen -dm -S mavproxy "+home+"/companion/scripts/start_mavproxy_telem_splitter.sh")
