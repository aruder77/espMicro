from controller import Controller
from espvent_device import EspVentDevice

class EspVentController(Controller):
    def __init__(self):
        super().__init__()

    def createHomieDevice(self, settings):
        return EspVentDevice(settings)
