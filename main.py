import sys
import time, machine, network, gc
import os

sys.path.append('/app')
sys.path.append('/app/lib')

from ota_initializer import connectToWifi, update
from esp_vent_controller import EspVentController


def main():
    connectToWifi()
    update()

    # start application controller
    controller = EspVentController()
    controller.run()


if __name__ == "__main__":
    main()
