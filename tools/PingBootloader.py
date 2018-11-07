#!/usr/bin/python -u

# This is a python script that will flash new firmware to
# a Blue Robotics Ping1D acoustic rangefinder.

# The goto_bootloader message is sent to the Ping1D device,
# which will then enter the stm32 serial bootloader. The
# firmware is then loaded using the stm32flash tool from
# https://git.code.sf.net/p/stm32flash/code. When the upload
# is complete, execution of the new program begins.

# It is possible that the device is currently being used
# by the proxy server application that is installed with the
# Blue Robotics companion computer repository. In this case,
# we shut down the proxy before communicating with the device
# then restart the proxy when we are finished

from brping import Ping1D, PingMessage, pingmessage
import platform
import time
import os
from argparse import ArgumentParser

parser = ArgumentParser(description=__doc__)
parser.add_argument("-d", dest="device", required=True, help="Serial port of the device to flash")
parser.add_argument("-b", dest="baudrate", type=int, default=115200, help="Baudrate of Ping1D's current firmware")
parser.add_argument("-f", dest="file", required=True, help="Binary or hex file to flash")
parser.add_argument("-v", dest='verifyOption', action='store_true', help="Verify firmware after writing to device")
args = parser.parse_args()

supported_machines = ('x86_64', 'armv7l')
machine = platform.machine()
if machine not in supported_machines:
    print(machine, 'cpu architecture is not supported')
    exit(1)

# stop pingproxy
print("Stopping proxy server...")
os.system("screen -X -S pingproxy quit")

# Connect to Ping
myPing = Ping1D(args.device, args.baudrate)

# Make sure we have a Ping on the line
if myPing.initialize() is False:
    print('Could not communicate with Ping device!')
    exit(1)

# send ping device to bootloader
print("Sending device to bootloader...")
bootloader_msg = PingMessage(pingmessage.PING1D_GOTO_BOOTLOADER)
bootloader_msg.pack_msg_data()
myPing.iodev.write(bootloader_msg.msg_data)

#TODO check for ack here

options = ''

if args.verifyOption is True:
    options += '-v'

print("Attempting to load new program...")
# Try five times, maybe not necessary
for x in range (0,5):
    time.sleep(0.5)
    cmd = '$COMPANION_DIR/tools/stm32flash_' + machine + ' ' + options + ' -g 0x0 -b 115200 -w ' + args.file + ' ' + args.device
    if os.system(cmd) == 0:
        break

print("Restarting proxy server...")
os.system("screen -dm -S pingproxy python -m Ping/PingProxy --device " + args.device)

print("Done")
