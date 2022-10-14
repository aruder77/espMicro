#!/bin/bash

# copy microhomie
mkdir .lib/homie/ || echo 'lib/homie already exists'
cp -r ../microhomie/homie/* .lib/homie/
cp -r ../microhomie/lib/primitives .lib/
cp ../micropython-mqtt/mqtt_as/mqtt_as.py .lib/

# copy wifimgr
cp ../WiFiManager/wifimgr.py .lib/esp_micro/

# copy ota_updater
cp ../micropython-ota-updater/app/ota_updater.py .lib/ota_updater/
cp ../micropython-ota-updater/app/httpclient.py .lib/ota_updater/

# copy ili9341 driver
cp ../micropython-ili9341/ili9341.py .lib/
cp ../micropython-ili9341/xglcd_font.py .lib/