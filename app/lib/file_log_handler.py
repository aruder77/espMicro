import uasyncio as asyncio

from logging import Handler
from logging import LogRecord

class FileLogHandler(Handler):

    _i = 0

    def __init__(self, device, loggerName):
        super().__init__()
        self.device = device
        self.loggerName = loggerName
        

    def emit(self, record: LogRecord):
        d = record.__dict__
        topic = self.device.dtopic + "/logging/" + self.loggerName
        value = d['levelname'] + ":" + d['name'] + ":" + d['message']
        self.file=open("%s.%d.log" % (self.loggerName, self._i), "a+")
        self.file.write("%s: %s\n" %(topic, value))
        self.file.close()
        self._i = self._i + 1
        
