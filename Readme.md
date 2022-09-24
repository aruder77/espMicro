# howto build

This basically follows this guide: https://github.com/micropython/micropython/blob/master/ports/esp32/README.md

## setup esp-idf

- git clone -b v4.2 --recursive https://github.com/espressif/esp-idf.git
- cd esp-idf
- ./install.sh
- source export.sh (needs to be called in every session)

## build micropython image

- clone micropython from git@github.com:micropython/micropython.git
- adjust path in copyLibToMicroPython.sh to point to this repo
- ./copyLibToMicroPython.sh
- in micropython repo
- make -C mpy-cross
- cd ports/esp32
- make submodules
- make
- export PORT=<usb-port with esp32>
- make erase
- make deploy

## upload project

- upload project using pymakr as usual

# Usage

## Configuration

After install config mode is automatically entered. You can enter config mode by pressing 'BOOT' button for more than 3 seconds.

- connect to 'WifiManager' WLAN using key 'tayfunulu'
- open http://192.168.4.1/
- enter all config and press save

## Remote software update

- current github-repo used: aruder77/espMicro
- development versions: releases (no draft!) of format vX.Y.Z
- release versions: releases of format rX.Y.Z

# TODOs

- expose release-version as property
- manually trigger remote-update
- remember config values in config mode

# Unsorted

- micropython auschecken
- mit 'copyLibToMicroPython.sh' libs nach micropython/ports/esp32/modules kopieren
- micropython bauen
  - in root dir (micropython dir)
  - docker run --rm -v $PWD:/project -w /project -it espressif/idf:release-v4.4
    - einmalig:
      - make -C mpy-cross
    - cd ports/esp32
      - make clean
      - make submodules
      - make
- micropython flashen
  - docker container verlassen
  - esptool.py -p /dev/tty.usbserial-0001 erase_flash
  - in micropython/ports/esp32:
    - esptool.py --chip esp32 --port /dev/tty.usbserial-0001 --baud 460800 write_flash -z 0x1000 build-GENERIC/firmware.bin
- espMicro repo in VS-Code und pymakr öffnen
- espMicro auf device syncen (espMicro enthält EspVent im moment)
