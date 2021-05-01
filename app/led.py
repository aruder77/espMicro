from homie.constants import FALSE, TRUE, BOOLEAN
from homie.node import HomieNode
from homie.property import HomieProperty
from machine import Pin
from esp_micro_node import EspMicroNode

class LED(EspMicroNode):

    # Reversed values for the esp8266 boards onboard led
    ONOFF = {FALSE: 1, TRUE: 0}

    def __init__(self, name="Onboard LED", pin=4):
        super().__init__(id="led", name=name, type="LED")
        self.led = Pin(pin, Pin.OUT, value=1)


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
