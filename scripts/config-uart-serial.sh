#!/usr/bin/env bash

# Remove any console definitions on serial0
sed -i 's/ console=serial0,115200//' /boot/cmdline.txt
