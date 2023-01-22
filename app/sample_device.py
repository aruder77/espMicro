from homie.device import HomieDevice, await_ready_state
from homie.node import HomieNode
from homie.property import HomieProperty
from utime import time
from homie.constants import FALSE, TRUE, BOOLEAN
from machine import Pin
from sys import platform


class SampleDevice(HomieDevice):

    ONOFF = {FALSE: 0, TRUE: 1}
    LED_PIN = 2 if platform == "esp32" else "LED"

    def __init__(self, settings):
        super().__init__(settings)
        self.led = Pin(self.LED_PIN, Pin.OUT, value=1)

        # Initialize the Homie node for the onboard LED
        led_node = HomieNode(id="led", name="Onboard LED", type="LED",)

        # Initialize the Homie property to power on/off the led
        led_power = HomieProperty(
            id="power",
            name="Power",
            settable=True,
            datatype=BOOLEAN,
            default=TRUE,
            on_message=self.on_power_msg
        )

        # Add the power property to the node
        led_node.add_property(led_power)

        # Add the led node to the device
        self.add_node(led_node)

    def on_power_msg(self, topic, payload, retained):
        print('Received LED set command!')
        self.led(self.ONOFF[payload])



