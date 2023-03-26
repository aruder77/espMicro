import settings
import network

from machine import Pin
import machine
from primitives.pushbutton import Pushbutton
from esp_micro.ota_initializer import update
from esp_micro.wifimgr import do_connect, get_connection

from esp_micro.config_loader import read_profiles, read_mqtt, configured


class EspMicroController:

    def __init__(self):
        # setup boot button for config mode
        print("setting up push button...")
        self.btn = Pushbutton(Pin(13, Pin.IN, Pin.PULL_UP))
        self.btn.long_func(self.enterConfigMode)

        print("checking for connected")
        # read saved wifi and mqtt data
        if not configured():
            print("not configured, entering configuration mode")
            get_connection()

        profiles = read_profiles()
        settings.WIFI_SSID = list(profiles.keys())[0]
        settings.WIFI_PASSWORD = profiles[settings.WIFI_SSID]
        connected = do_connect(settings.WIFI_SSID, settings.WIFI_PASSWORD)

        # read mqtt data
        (settings.MQTT_BROKER, settings.MQTT_USER, settings.MQTT_PASSWORD, githubRepo, autoUpdate,
         unstableVersions) = read_mqtt()
        if (connected is not False) and autoUpdate:
            update(unstableVersions)

        settings.DEVICE_ID = self.getDeviceID()
        settings.DEVICE_NAME = self.getDeviceName()

        # Homie device setup
        self.homie = self.createHomieDevice(settings)

    def createHomieDevice(self, settings, ssid, password, mqttServer, mqttUser, mqttPassword):
        print('You must override this method and return an EspMicroDevice subclass!')

    def getDeviceName(self):
        print('You must override this method and return a device name!')

    def getDeviceID(self):
        print('You must override this method and return a device ID!')

    def run(self):
        # run forever
        self.homie.run_forever()

    def enterConfigMode(self):
        print("entering config mode...")
        with open('configMode', "w") as f:
            f.write('config')
        machine.reset()
