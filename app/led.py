from homie.constants import FALSE, TRUE, BOOLEAN
from homie.node import HomieNode
from homie.property import HomieProperty
from esp_micro_node import EspMicroNode

class LED(EspMicroNode):

    # Reversed values for the esp8266 boards onboard led
    ONOFF = {FALSE: 1, TRUE: 0}

    def __init__(self, device, id=0, name="Onboard LED", pin=0):
        super().__init__(device, id="led%d" % id, name=name, type="LED")
        #self.led = Pin(pin, Pin.OUT, value=1)

        # Boot button on some dev boards
        #self.btn = Pushbutton(Pin(pin, Pin.IN, Pin.PULL_UP))
        #self.btn.press_func(self.toggle_led)

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
        #self.led(self.ONOFF[payload])
        pass

    def toggle_led(self):
        if self.p_power.value == TRUE:
            #self.led(1)
            self.p_power.value = False
        else:
            #self.led(0)
            self.p_power.value = True