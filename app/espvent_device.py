from app.MotorsNode import MotorsNode
from esp_micro_device import EspMicroDevice
from utime import time
from MotorNode import MotorNode
from led import LED


class EspVentDevice(EspMicroDevice):

    def __init__(self, settings, ssid, password, mqttServer, mqttUser, mqttPassword):
        super().__init__(settings, ssid, password, mqttServer, mqttUser, mqttPassword)
        #self.logger = self.getLogger()

        motorNodes = [
            MotorNode(self, 4, 1, False),
            MotorNode(self, 13, 2, True),
            MotorNode(self, 14, 3, False),
            MotorNode(self, 27, 4, True),
            MotorNode(self, 26, 5, False),
            MotorNode(self, 25, 6, True),
            MotorNode(self, 33, 7, False),
            MotorNode(self, 32, 8, True)
        ]
        for motorNode in motorNodes:
            self.add_node(motorNode)
        
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



    async def everySecond(self):
        print ('.', end='')
