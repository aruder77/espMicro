from app.MotorsNode import MotorsNode
from homie.device import HomieDevice, await_ready_state
from utime import time
from MotorNode import MotorNode


class EspVentDevice(HomieDevice):

    def __init__(self, settings):
        super().__init__(settings)

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

        self.add_node(MotorsNode(motorNodes))