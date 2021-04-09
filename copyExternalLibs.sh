#!/bin/bash

# copy microhomie
cp -r ../microhomie/homie lib/
cp -r ../microhomie/lib/primitives lib/
cp ../microhomie/lib/mqtt_as.py lib/

# copy wifimgr
cp ../WiFiManager/wifimgr.py lib/

# copy ota_updater
cp ../micropython-ota-updater/app/ota_updater.py lib/
cp ../micropython-ota-updater/app/httpclient.py lib/