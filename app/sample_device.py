from homie.device import HomieDevice, await_ready_state
from homie.node import HomieNode
from homie.property import HomieProperty
from utime import time


class SampleDevice(HomieDevice):

    def __init__(self, settings):
        super().__init__(settings)

        # Initialize the Homie node for the onboard LED
        led_node = HomieNode(id="led", name="Onboard LED", type="LED",)

        # Initialize the Homie property to power on/off the led
        led_power = HomieProperty(
            id="power",
            name="Power",
            settable=True,
            datatype=BOOLEAN,
            default=FALSE,
            on_message=toggle_led,
        )

        # Add the power property to the node
        led_node.add_property(led_power)

        # Add the led node to the device
        self.add_node(led_node)



