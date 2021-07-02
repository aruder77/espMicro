from homie.node import HomieNode

class EspMicroNode(HomieNode):
    def __init__(self, device, id, name, type):
        super().__init__(id, name, type)
        #self.device = device

    async def every100Milliseconds(self):
        pass

    async def everySecond(self):
        pass

    async def every10Seconds(self):
        pass

    async def everyMinute(self):
        pass

    async def everyHour(self):
        pass

    async def everyDay(self):
        pass

    def getLogger(self):
        return self.device.getLogger()