import sys
import time, machine, network, gc
import os

sys.path.append('/app')
sys.path.append('/app/lib')

from controller import Controller
import wifimgr
from config_loader import read_mqtt
from ota_updater.ota_updater import OTAUpdater


otaUpdater = None

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


def main():
    connectToWifi()
    update()

    # start application controller
    controller = Controller(otaUpdater)
    controller.run()


if __name__ == "__main__":
    main()
