from esp_micro.esp_micro_controller import EspMicroController
from sample_device import SampleDevice

class MainController(EspMicroController):
    def __init__(self):
        super().__init__()

    def createHomieDevice(self, settings):
        return SampleDevice(settings)

    def getDeviceName(self):
        return 'sampleDevice'

    def getDeviceID(self):
        return 'sampleDevice'
