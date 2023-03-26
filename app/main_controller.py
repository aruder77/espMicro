from esp_micro.esp_micro_controller import EspMicroController
from sample_device import SampleDevice


class MainController(EspMicroController):

    def __init__(self):
        super().__init__()

    def create_homie_device(self, settings):
        return SampleDevice(settings)

    def get_device_name(self):
        return 'sampleDevice'

    def get_device_id(self):
        return 'sampleDevice'
