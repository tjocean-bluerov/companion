#!/usr/bin/env bash

# Remove any console definitions on serial0
sed -i 's/ console=serial0,[0-9]\+//g' /boot/cmdline.txt

# Append a single console definition to the end of the line
sed -i "s/.*/& console=serial0,115200/" /boot/cmdline.txt
