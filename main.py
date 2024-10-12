import sys
import time, machine, network, gc
import os

import esp_micro.esp_micro_controller as esp_micro_controller

sys.path.append('/app')
sys.path.append('/app/.lib')

from main_controller import MainController

def main():
    # start application controller
    controller = MainController()
    esp_micro_controller.controller = controller
    controller.run()


if __name__ == "__main__":
    main()
