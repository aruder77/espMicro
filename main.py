import wifimgr
from app.controller import Controller
import time, machine, network, gc
from ota_updater.ota_updater import OTAUpdater
import os

MQTT_PROFILE = 'mqtt.dat'

otaUpdater = None

def connectToWifiAndUpdate():
    time.sleep(1)
    print('Memory free', gc.mem_free())

    githubRepo = read_mqtt()
    otaUpdater = OTAUpdater(githubRepo, main_dir='app')
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        machine.reset()
    else:
        del(otaUpdater)
        gc.collect()

def read_mqtt():
    with open(MQTT_PROFILE) as f:
        lines = f.readlines()
    githubRepo = lines[3].strip("\n").split(";")[1].replace('%2F', '/').replace('%3A', ':')
    return githubRepo

def main():
    if 'configMode.txt' in os.listdir('/'):
        os.remove('configMode.txt')
        wifimgr.start()
    wlan = wifimgr.get_connection()
    if wlan is None:
        print("Could not initialize the network connection.")
        while True:
            pass  # you shall not pass :D

    connectToWifiAndUpdate()

    # start application controller
    controller = Controller(otaUpdater)
    controller.run()


if __name__ == "__main__":
    main()
