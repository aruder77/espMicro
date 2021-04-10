import settings
import network

from machine import Pin
import machine
from primitives.pushbutton import Pushbutton

from myhomie import MyHomieDevice
from app.led import LED

NETWORK_PROFILES = 'wifi.dat'
MQTT_PROFILE = 'mqtt.dat'

class Controller:

    def __init__(self, otaUpdater):
        self.otaUpdater = otaUpdater

        # setup boot button for config mode
        self.btn = Pushbutton(Pin(0, Pin.IN, Pin.PULL_UP))
        self.btn.long_func(self.enterConfigMode)

        # read saved wifi and mqtt data
        profiles = self.read_profiles()
        wlan = network.WLAN(network.STA_IF)
        ssid = wlan.config('essid')
        password = profiles[ssid]
        (mqttServer, mqttUser, mqttPassword, githubRepo) = self.read_mqtt()        

        # Homie device setup
        self.homie = MyHomieDevice(settings, ssid, password, mqttServer, mqttUser, mqttPassword, githubRepo)

        # Add LED node to device
        self.homie.add_node(LED())

    def run(self):
        # run forever
        self.homie.run_forever()

    def read_profiles(self):
        with open(NETWORK_PROFILES) as f:
            lines = f.readlines()
        profiles = {}
        for line in lines:
            ssid, password = line.strip("\n").split(";")
            profiles[ssid] = password
        return profiles

    def read_mqtt(self):
        with open(MQTT_PROFILE) as f:
            lines = f.readlines()
        mqttServer  = lines[0].strip("\n").split(";")[1]
        mqttUser  = lines[1].strip("\n").split(";")[1]
        mqttPassword  = lines[2].strip("\n").split(";")[1]
        return (mqttServer, mqttUser, mqttPassword)   

    def enterConfigMode(self):
        print("entering config mode...")
        with open('configMode.txt', "w") as f:
            f.write('config')
        machine.reset()







 






