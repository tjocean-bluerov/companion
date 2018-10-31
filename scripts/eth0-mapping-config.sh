#!/usr/bin/env bash

if [ -f "/home/pi/network.conf" ]; then 
    cat /home/pi/network.conf
else
    echo "config-manual"
fi
