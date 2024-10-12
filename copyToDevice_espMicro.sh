#!/bin/bash
export DEVICE=/dev/cu.usbmodem2101
mpremote connect $DEVICE fs cp -r lib/esp_micro :
