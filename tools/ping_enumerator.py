#!/usr/bin/env python -u

"""Scan serial ports for ping devices
    Symlinks to detected devices are created under /dev/serial/ping/
    This script needs root permission to create the symlinks
    Exits with the number of ping devices detected
"""
import subprocess
from brping import Ping1D

def main():
    """Main function
        Enumerate new ping devices
    """
    output = ""
    # Remove any previously created links
    try:
        output = subprocess.check_output(["rm", "-rf", "/dev/serial/ping"])
    except subprocess.CalledProcessError as exception:
        print(exception)

    # Look for connected serial devices
    try:
        output = subprocess.check_output("ls /dev/serial/by-id", shell=True)
    except subprocess.CalledProcessError as exception:
        print(exception)
        exit(1)

    pings_found = 0

    # Look at each serial device, probe for ping
    for dev in output.split('\n'):
        if not dev:
            continue

        byiddev = "/dev/serial/by-id/" + dev

        print("Looking for Ping at %s" % byiddev)
        new_ping = Ping1D(byiddev)

        if not new_ping.initialize():
            continue

        try:
            if new_ping.get_device_id() and new_ping.get_fw_version():
                # ex Ping1D-id-43-t-1-m-1-v-3.19
                description = "/dev/serial/ping/Ping1D-id-%s-t-%s-m-%s-v-%s.%s" % (
                    new_ping._device_id,
                    new_ping._device_type,
                    new_ping._device_model,
                    new_ping._fw_version_major,
                    new_ping._fw_version_minor
                    )
                print("Found Ping1D (ID: %d) at %s" % (new_ping._device_id, dev))

                # Follow link to actual device
                target_device = subprocess.check_output(' '.join(["readlink", "-f", byiddev]), shell=True)
                # Strip newline from output
                target_device = target_device.split('\n')[0]

                # Create another link to it
                print("Creating symbolic link to", target_device)
                subprocess.check_output(' '.join(["mkdir", "-p", "/dev/serial/ping"]), shell=True)
                output = subprocess.check_output("ln -fs %s %s" % (
                    target_device,
                    description), shell=True)
                pings_found += 1

        except subprocess.CalledProcessError as exception:
            print(exception)
            continue

    exit(pings_found)

if __name__ == '__main__':
    main()
