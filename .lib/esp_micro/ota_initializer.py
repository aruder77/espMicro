import sys
import time, machine, gc
import os

import esp_micro.wifimgr
from esp_micro.config_loader import read_mqtt
from ota_updater.ota_updater import OTAUpdater


def update(unstableVersions: bool):
    time.sleep(1)
    print('Memory free', gc.mem_free())

    githubRepo = read_mqtt()[3]
    
    otaUpdater = OTAUpdater(githubRepo, main_dir='app', unstableVersions=unstableVersions)
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        machine.reset()
    else:
        del(otaUpdater)
        gc.collect()


def connectToWifi():
    if 'configMode' in os.listdir('/'):
        os.remove('configMode')
        esp_micro.wifimgr.start()
    wlan = esp_micro.wifimgr.get_connection()
    if wlan is None:
        print("Could not initialize the network connection.")
        while True:
            pass  # you shall not pass :D