import uasyncio as asyncio

from logging import Handler
from logging import LogRecord

class MqttLogHandler(Handler):

    def __init__(self, device, loggerName):
        super().__init__()
        self.device = device
        self.loggerName = loggerName

    def emit(self, record: LogRecord):
        d = record.__dict__
        topic = self.device.dtopic + "/logging/" + self.loggerName
        value = d['levelname'] + ":" + d['name'] + ":" + d['message']
        asyncio.create_task(
            self.device.publish(topic,value)
        )
        
