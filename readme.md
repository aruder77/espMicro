# howto build 

This basically follows this guide: https://github.com/micropython/micropython/blob/master/ports/esp32/README.md

## setup esp-idf

* git clone -b v4.2 --recursive https://github.com/espressif/esp-idf.git
* cd esp-idf
* ./install.sh
* source export.sh (needs to be called in every session)

## build micropython image

* clone micropython from git@github.com:micropython/micropython.git
* adjust path in copyLibToMicroPython.sh to point to this repo
* ./copyLibToMicroPython.sh
* in micropython repo
* make -C mpy-cross 
* cd ports/esp32
* make submodules
* make
* export PORT=<usb-port with esp32>
* make erase
* make deploy

## upload project

* upload project using pymakr as usual

# Usage

## Configuration

After install config mode is automatically entered. You can enter config mode by pressing 'BOOT' button for more than 3 seconds.

* connect to 'WifiManager' WLAN using key 'tayfunulu'
* open http://192.168.4.1/
* enter all config and press save

## Remote software update

* current github-repo used: aruder77/espMicro
* development versions: releases (no draft!) of format vX.Y.Z
* release versions: releases of format rX.Y.Z

# TODOs

* expose release-version as property
* manually trigger remote-update
* remember config values in config mode
