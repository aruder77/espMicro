from machine import Pin


class MicrocontrollerConfig:

    def __init__(self):
        pass

    def getLedPin(self):
        return "LED"

    def getButtonPin(self):
        return 13

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
    
    def getDisplayLedPin(self):
        return 12

    def getSDCardCSPin(self):
        return 22

    def getTouchCSPin(self):
        return 15

    def getTouchIRQPin(self):
        return 14
    
    def getSpi(self):
        return 0 


class RP2PicoConfig(MicrocontrollerConfig):

    def __init__(self):
        super()


class ArduinoNanoConnectConfig(MicrocontrollerConfig):

    def __init__(self):
        super()

    def getLedPin(self):
        return 6


class Esp32NodeMcuConfig(MicrocontrollerConfig):

    def __init__(self):
        super()

    def getLedPin(self):
        return 12

    def getButtonPin(self):
        return 14

    def getSCKPin(self):
        return 18

    def getMOSIPin(self):
        return 23

    def getMISOPin(self):
        return 19

    def getDisplayCSPin(self):
        return 15

    def getDisplayResetPin(self):
        return 4

    def getDisplayDCPin(self):
        return 2
    
    def getDisplayLedPin(self):
        return 5

    def getSDCardCSPin(self):
        return 5

    def getTouchCSPin(self):
        return 21

    def getTouchIRQPin(self):
        return 22
    
    def getSpi(self):
        return 2

    
class Esp32WroverKitConfig(MicrocontrollerConfig):

    def __init__(self):
        super()

    def getLedPin(self):
        return 2

    def getButtonPin(self):
        return 14

    def getSCKPin(self):
        return 19

    def getMOSIPin(self):
        return 23

    def getMISOPin(self):
        return 25

    def getDisplayCSPin(self):
        return 22

    def getDisplayResetPin(self):
        return 18

    def getDisplayDCPin(self):
        return 21
    
    def getDisplayLedPin(self):
        return 5

    def getSDCardCSPin(self):
        return 5

    def getTouchCSPin(self):
        return 21

    def getTouchIRQPin(self):
        return 22    
    
    def getSpi(self):
        return 2
