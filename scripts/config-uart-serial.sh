#!/usr/bin/env bash

# Remove any console definitions on serial0
sed -i 's/ console=serial0,[0-9]\+//g' /boot/cmdline.txt
