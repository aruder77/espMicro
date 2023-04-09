#!/bin/bash
export DEVICE=/dev/cu.usbmodem2101
mpremote connect $DEVICE fs cp -r app :
mpremote connect $DEVICE fs cp -r lib :
mpremote connect $DEVICE fs cp -r fonts :
mpremote connect $DEVICE fs mkdir :main
mpremote connect $DEVICE fs cp bootstrap/main/.version :main/.version
mpremote connect $DEVICE fs cp bootstrap/mqtt.dat :mqtt.dat
mpremote connect $DEVICE fs cp bootstrap/wifi.dat :wifi.dat
mpremote connect $DEVICE fs cp main.py :
mpremote connect $DEVICE fs cp boot.py :
mpremote connect $DEVICE fs cp settings.py :