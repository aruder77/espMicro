from machine import Pin


class MicrocontrollerConfig:

    def __init__(self):
        pass

    def getLedPin(self):
        return "LED"

    def getButtonPin(self):
        return 20

    def getSCKPin(self):
        return 18

    def getMOSIPin(self):
        return 19

    def getMISOPin(self):
        return 16

    def getDisplayCSPin(self):
        return 17

    def getDisplayResetPin(self):
        return 20

    def getDisplayDCPin(self):
        return 21

    def getSDCardCSPin(self):
        return 22

    def getTouchCSPin(self):
        return 26

    def getTouchIRQPin(self):
        return 27


class RP2PicoConfig(MicrocontrollerConfig):

    def __init__(self):
        super()


class ArduinoNanoConnectConfig(MicrocontrollerConfig):

    def __init__(self):
        super()

    def getLedPin(self):
        return 6


class Esp32Config(MicrocontrollerConfig):

    def __init__(self):
        super()