from esp_micro_device import EspMicroDevice
from utime import time

class MyDevice(EspMicroDevice):

    def __init__(self, settings, ssid, password, mqttServer, mqttUser, mqttPassword):
        super().__init__(settings, ssid, password, mqttServer, mqttUser, mqttPassword)
        self.logger = self.getLogger()

    async def everySecond(self):
        print ('.', end='')
