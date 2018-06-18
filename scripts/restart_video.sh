#!/bin/bash

if screen -ls | grep video; then
        screen -X -S video quit
fi

if [ -z "$1" ]; then
    sudo -H -u pi screen -dm -S video /home/pi/companion/tools/streamer.py
else
    sudo -H -u pi screen -dm -S video /home/pi/companion/tools/streamer.py $1 $2 $3 $4
fi



