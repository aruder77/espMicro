import sys
import time, machine, gc
import os

import wifimgr
from config_loader import read_mqtt
from ota_updater.ota_updater import OTAUpdater


def update():
    time.sleep(1)
    print('Memory free', gc.mem_free())

    githubRepo = read_mqtt()[3]
    
    otaUpdater = OTAUpdater(githubRepo, main_dir='app')
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        machine.reset()
    else:
        del(otaUpdater)
        gc.collect()


def connectToWifi():
    if 'configMode' in os.listdir('/'):
        os.remove('configMode')
        wifimgr.start()
    wlan = wifimgr.get_connection()
    if wlan is None:
        print("Could not initialize the network connection.")
        while True:
            pass  # you shall not pass :D