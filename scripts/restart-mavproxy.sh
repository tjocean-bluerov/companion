#!/bin/bash

screen -X -S mavproxy quit
sudo -H -u pi screen -dm -S mavproxy \
    $COMPANION_DIR/tools/telem.py
