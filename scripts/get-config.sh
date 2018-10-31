#!/usr/bin/env bash

if [[ $(< /home/pi/network.conf) == "config-manual" ]]; then
	echo "Manual"
	exit 0
fi
if [[ $(< /home/pi/network.conf) == "config-server" ]]; then
	echo "DHCP Server"
	exit 0
fi
if [[ $(< /home/pi/network.conf) == "config-client" ]]; then 
	echo "DHCP Client"
	exit 0
fi
