#!/bin/bash

if screen -ls | grep video; then
        screen -X -S video quit
fi

# this is followed up in start_video.sh
cp /home/pi/vidformat.param /home/pi/vidformat.param.bak

echo $1 > /home/pi/vidformat.param
echo $2 >> /home/pi/vidformat.param
echo $3 >> /home/pi/vidformat.param
echo $4 >> /home/pi/vidformat.param

sudo -H -u pi screen -dm -S video /home/pi/companion/tools/streamer.py


