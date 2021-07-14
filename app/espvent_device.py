from app.MotorsNode import MotorsNode
from homie.device import HomieDevice, await_ready_state
from utime import time
from MotorNode import MotorNode
import uasyncio as asyncio
from uasyncio import sleep_ms

WORKER_DELAY = const(100)

class EspVentDevice(HomieDevice):

    counter = 0

    def __init__(self, settings):
        super().__init__(settings)
        #self.logger = self.getLogger()

        motorNodes = [
            MotorNode(4, 1, False),
            MotorNode(13, 2, True),
            MotorNode(14, 3, False),
            MotorNode(27, 4, True),
            MotorNode(26, 5, False),
            MotorNode(25, 6, True),
            MotorNode(33, 7, False),
            MotorNode(32, 8, True)
        ]
        for motorNode in motorNodes:
            self.add_node(motorNode)

        asyncio.create_task(self.workerLoop())            
        
        #self.add_node(MotorsNode(self, motorNodes))
        #self.add_node(LED(self))
        #self.add_node(LED(self,1, "LED 1"))
        #self.add_node(LED(self,2, "LED 2"))
        #self.add_node(LED(self,3, "LED 3"))
        #self.add_node(LED(self,4, "LED 4"))
        #self.add_node(LED(self,5, "LED 5"))
        #self.add_node(LED(self,6, "LED 6"))
        #self.add_node(LED(self,7, "LED 7"))
        #self.add_node(LED(self,8, "LED 8"))
        #self.add_node(LED(self,9, "LED 9"))
        #self.add_node(LED(self,10, "LED 10"))
        #self.add_node(LED(self,11, "LED 11"))
        #self.add_node(LED(self,12, "LED 12"))
        #self.add_node(LED(self,13, "LED 13"))
        #self.add_node(LED(self,14, "LED 14"))


    @await_ready_state
    async def workerLoop(self):
        counter = 0
        while True: 
            self.loop()

            await sleep_ms(WORKER_DELAY)


    def loop(self):
        if  self.counter % 10 == 0:
            print ('.', end='')
            self.counter = 0
        self.counter += 1
