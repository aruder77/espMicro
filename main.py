import sys
import time, machine, network, gc
import os

sys.path.append('/app')
sys.path.append('/app/lib')

from espvent_controller import EspVentController

def main():
    # start application controller
    controller = EspVentController()
    controller.run()


if __name__ == "__main__":
    main()
