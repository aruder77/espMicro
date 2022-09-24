#!/bin/bash

# copy microhomie
mkdir .lib/homie/ || echo 'lib/homie already exists'
cp -r ../microhomie/homie/* .lib/homie/
cp -r ../microhomie/lib/primitives .lib/
cp ../microhomie/lib/mqtt_as.py .lib/

# copy wifimgr
# don't copy, since modified (added mqtt settings)
# cp ../WiFiManager/wifimgr.py lib/

# copy ota_updater
cp ../micropython-ota-updater/app/ota_updater.py .lib/ota_updater/
cp ../micropython-ota-updater/app/httpclient.py .lib/ota_updater/