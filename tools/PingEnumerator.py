#!/usr/bin/python -u

# Scan serial ports for ping devices
# Symlinks to detected devices are created under /dev/serial/ping/
# This script needs root permission to create the symlinks
# Exits with the number of ping devices detected

from Ping import Ping1D
import subprocess

# Remove any previously created links
try:
    output = subprocess.check_output(["rm", "-rf", "/dev/serial/ping"])
except subprocess.CalledProcessError as e:
    print e

# Look for connected serial devices
try:
    output = subprocess.check_output("ls /dev/serial/by-id", shell=True)
except subprocess.CalledProcessError as e:
    print e
    exit(0)

pings_found = 0

# Look at each serial device, probe for ping
for dev in output.split('\n'):
    if len(dev) > 0:
        byiddev = "/dev/serial/by-id/" + dev

        print("Looking for Ping at %s" % byiddev)
        newPing = Ping1D.Ping1D(byiddev)

        if newPing.initialize() == True:
            try:
                if newPing.get_device_id() != None and newPing.get_fw_version() != None:

                    # ex Ping1D-id-43-t-1-m-1-v-3.19
                    description = "/dev/serial/ping/Ping1D-id-%s-t-%s-m-%s-v-%s.%s" % (newPing.device_id, newPing.device_type, newPing.device_model, newPing.fw_version_major, newPing.fw_version_minor)
                    print "Found Ping1D (ID: %d) at %s" % (newPing.device_id, dev)

                    # Follow link to actual device
                    target_device = subprocess.check_output("readlink -f " + byiddev, shell=True)
                    # Strip newline from output
                    target_device = target_device.split('\n')[0]

                    # Create another link to it
                    print "Creating symbolic link to", target_device
                    subprocess.check_output("mkdir -p /dev/serial/ping", shell=True)
                    output = subprocess.check_output("ln -fs " + target_device + " " + description, shell=True)
                    pings_found += 1

            except subprocess.CalledProcessError as e:
                print e
                continue

exit(pings_found)
