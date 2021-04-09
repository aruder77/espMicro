import settings

from machine import Pin
from primitives.pushbutton import Pushbutton

from homie.constants import FALSE, TRUE, BOOLEAN
from homie.device import HomieDevice
from homie.node import HomieNode
from homie.property import HomieProperty
from myhomie import MyHomieDevice

NETWORK_PROFILES = 'wifi.dat'
MQTT_PROFILE = 'mqtt.dat'


class LED(HomieNode):

    # Reversed values for the esp8266 boards onboard led
    ONOFF = {FALSE: 1, TRUE: 0}

    def __init__(self, name="Onboard LED", pin=0):
        super().__init__(id="led", name=name, type="LED")
        self.led = Pin(pin, Pin.OUT, value=1)

        # Boot button on some dev boards
        self.btn = Pushbutton(Pin(pin, Pin.IN, Pin.PULL_UP))
        self.btn.press_func(self.toggle_led)

        self.p_power = HomieProperty(
            id="power",
            name="LED Power",
            settable=True,
            datatype=BOOLEAN,
            default=FALSE,
            on_message=self.on_power_msg,
        )
        self.add_property(self.p_power)

    def on_power_msg(self, topic, payload, retained):
        self.led(self.ONOFF[payload])

    def toggle_led(self):
        if self.p_power.value == TRUE:
            self.led(1)
            self.p_power.value = False
        else:
            self.led(0)
            self.p_power.value = True


def read_profiles():
    with open(NETWORK_PROFILES) as f:
        lines = f.readlines()
    profiles = {}
    for line in lines:
        ssid, password = line.strip("\n").split(";")
        profiles[ssid] = password
    return profiles

def read_mqtt():
    with open(MQTT_PROFILE) as f:
        lines = f.readlines()
    mqttServer  = lines[0].strip("\n").split(";")[1]
    mqttUser  = lines[1].strip("\n").split(";")[1]
    mqttPassword  = lines[2].strip("\n").split(";")[1]
    return (mqttServer, mqttUser, mqttPassword)    



# read saved wifi data
profiles = read_profiles()
ssid = wlan.config('essid')
password = profiles[ssid]
(mqttServer, mqttUser, mqttPassword) = read_mqtt()

# Homie device setup
homie = MyHomieDevice(settings, ssid, password, mqttServer, mqttUser, mqttPassword)

# Add LED node to device
homie.add_node(LED())

# run forever
homie.run_forever()

