import settings
import network

from machine import Pin
import machine
from primitives.pushbutton import Pushbutton

from myhomie import MyHomieDevice
from led import LED

from config_loader import read_profiles
from config_loader import read_mqtt


class Controller:

    def __init__(self, otaUpdater):
        self.otaUpdater = otaUpdater

        # setup boot button for config mode
        self.btn = Pushbutton(Pin(0, Pin.IN, Pin.PULL_UP))
        self.btn.long_func(self.enterConfigMode)

        # read saved wifi and mqtt data
        profiles = read_profiles()
        wlan = network.WLAN(network.STA_IF)
        ssid = wlan.config('essid')
        password = profiles[ssid]
        (mqttServer, mqttUser, mqttPassword, githubRepo) = read_mqtt()        

        # Homie device setup
        self.homie = MyHomieDevice(settings, ssid, password, mqttServer, mqttUser, mqttPassword)

        # Add LED node to device
        self.homie.add_node(LED())

    def run(self):
        # run forever
        self.homie.run_forever()


    def enterConfigMode(self):
        print("entering config mode...")
        with open('configMode', "w") as f:
            f.write('config')
        machine.reset()







 






