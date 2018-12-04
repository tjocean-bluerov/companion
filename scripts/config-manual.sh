#!/usr/bin/env bash

#copy the configuration information to network.conf
echo "config-manual" > /home/pi/network.conf
echo 192.168.2.2 > /home/pi/static-ip.conf
sudo reboot now
