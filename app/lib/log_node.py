from logging import getLogger
from esp_micro_node import EspMicroNode
from logging import Logger
from mqtt_log_handler import MqttLogHandler
from homie.property import HomieProperty
from homie.constants import INTEGER

class LogNode(EspMicroNode):

    _loggers = {}

    def __init__(self, device):
        super().__init__(id="log", name="logNode", type="LOG")
        self.device = device
                
        self.p_level = HomieProperty(
            id="level",
            name="Log Level",
            settable=True,
            datatype=INTEGER,
            default=20,
            on_message=self.on_level_msg,
        )
        self.add_property(self.p_level)

    def on_level_msg(self, topic, payload, retained):
        print('setting log level to %d' % int(payload))
        for l in self._loggers.values():
            l.setLevel(int(payload))

    def getLogger(self, name="root"):
        if name in self._loggers:
            return self._loggers[name]
        l = getLogger(name)
        l.addHandler(MqttLogHandler(self.device, name))
        #l.addHandler(FileLogHandler(self.device, name))
        self._loggers[name] = l
        return l





        
