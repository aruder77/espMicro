from controller import Controller
from mydevice import MyDevice

class EspVentController(Controller):
    def __init__(self):
        super().__init__()

    def createHomieDevice(self, settings, ssid, password, mqttServer, mqttUser, mqttPassword):
        return MyDevice(settings, ssid, password, mqttServer, mqttUser, mqttPassword)
