import time, machine, gc
import os

import esp_micro.wifimgr
from esp_micro.config_loader import read_mqtt
from esp_micro.logutil import get_logger
from ota_updater.ota_updater import OTAUpdater

class OtaInitializer:

    def __init__(self, autoUpdate: bool, unstableVersions: bool):
        self.logger = get_logger()

        self.githubRepo = read_mqtt()[3]

        self.otaUpdater = OTAUpdater(self.githubRepo, main_dir='app', unstableVersions=unstableVersions)
        self.autoUpdate = autoUpdate

    def update(self):
        time.sleep(1)
        self.logger.info('Memory free %d', gc.mem_free())

        if (self.autoUpdate):
            hasUpdated = self.otaUpdater.install_update_if_available()
        else:
            hasUpdated = self.otaUpdater.install_update_if_available_after_boot(None, None)

        if hasUpdated:
            machine.reset()
        else:
            gc.collect()

    def check_for_update_to_install_during_next_reboot(self):
        self.otaUpdater.check_for_update_to_install_during_next_reboot()

    def get_version(self):
        return self.otaUpdater.get_version('main')

def connectToWifi():
    if 'configMode' in os.listdir('/'):
        os.remove('configMode')
        esp_micro.wifimgr.start()
    get_logger().info('Connecting to WiFi...')
    wlan = esp_micro.wifimgr.get_connection()
    if wlan is None:
        get_logger().info("Could not initialize the network connection.")
        while True:
            pass  # you shall not pass :D