#!/usr/bin/env bash

#copy the configuration information to network-conf.txt
echo "config-server" > /home/pi/network.conf

#Bring down interface eth0
sudo ifdown eth0
echo "Interface eth0 is down"

#Bring up eth0 with DHCP Server configuration
sudo ifup eth0
echo "Interface eth0 is up with DHCP Server configuration"
echo "Configuration settings for dhcp-server mode applied to Companion"

#Restart dhcp server 
sudo service isc-dhcp-server restart

#Enable it to run at boot
sudo update-rc.d isc-dhcp-server defaults
echo "DHCP server enabled to run at boot"

sudo reboot now
