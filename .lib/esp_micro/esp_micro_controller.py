import settings
import network

from machine import Pin
import machine
from primitives.pushbutton import Pushbutton
from esp_micro.ota_initializer import connectToWifi, update


from esp_micro.config_loader import read_profiles
from esp_micro.config_loader import read_mqtt


class EspMicroController:

    def __init__(self):
        # setup boot button for config mode
        print("setting up push button...")
        self.btn = Pushbutton(Pin(0, Pin.IN, Pin.PULL_UP))
        self.btn.long_func(self.enterConfigMode)

        # connect to wifi
        connectToWifi()

        # read saved wifi and mqtt data
        profiles = read_profiles()
        wlan = network.WLAN(network.STA_IF)
        settings.WIFI_SSID = wlan.config('essid')
        settings.WIFI_PASSWORD = profiles[settings.WIFI_SSID]
        (settings.MQTT_BROKER, settings.MQTT_USER, settings.MQTT_PASSWORD, githubRepo, autoUpdate, unstableVersions) = read_mqtt()        
        if autoUpdate:
            update(unstableVersions)

        # Homie device setup
        self.homie = self.createHomieDevice(settings)


    def createHomieDevice(self, settings, ssid, password, mqttServer, mqttUser, mqttPassword):
        print('You must override this method and return an EspMicroDevice subclass!')


    def run(self):
        # run forever
        self.homie.run_forever()


    def enterConfigMode(self):
        print("entering config mode...")
        with open('configMode', "w") as f:
            f.write('config')
        machine.reset()







 






