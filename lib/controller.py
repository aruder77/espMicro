import settings
import network

from machine import Pin
import machine
from primitives.pushbutton import Pushbutton

from config_loader import read_profiles
from config_loader import read_mqtt


class Controller:

    def __init__(self):
        # setup boot button for config mode
        print("setting up push button...")
        self.btn = Pushbutton(Pin(0, Pin.IN, Pin.PULL_UP))
        self.btn.long_func(self.enterConfigMode)

        # read saved wifi and mqtt data
        profiles = read_profiles()
        wlan = network.WLAN(network.STA_IF)
        ssid = wlan.config('essid')
        password = profiles[ssid]
        (mqttServer, mqttUser, mqttPassword, githubRepo) = read_mqtt()        

        # Homie device setup
        self.homie = self.createHomieDevice(settings, ssid, password, mqttServer, mqttUser, mqttPassword)


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







 






