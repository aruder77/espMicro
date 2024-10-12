from machine import Pin, SPI
from micropython import const
from uasyncio import sleep, sleep_ms, create_task

from esp_micro.logutil import get_logger
from ili9341 import Display
from xglcd_font import XglcdFont
from esp_micro import singletons

YELLOW = const(0XFFE0)  # (255, 255, 0)
WHITE = const(0XFFFF)  # (255, 255, 255)
RED = const(0XF800)  # (255, 0, 0)
GREEN = const(0X07E0)  # (0, 255, 0)
BLUE = const(0X001F)  # (0, 0, 255)
BLACK = const(0)

SIZE_X = const(239)
SIZE_Y = const(319)


class DisplayController:

    def __init__(self):
        self.logger = get_logger()
        self.logger.info("initializing display...")

        disp_cs = Pin(singletons.microcontrollerConfig.getDisplayCSPin(), Pin.OUT)  # display shares spi
        led = Pin(singletons.microcontrollerConfig.getDisplayLedPin(), Pin.OUT)
        led.value(1)
        self.logger.info("LED pin %d", singletons.microcontrollerConfig.getDisplayLedPin())

        sck_pin = singletons.microcontrollerConfig.getSCKPin()
        mosi_pin = singletons.microcontrollerConfig.getMOSIPin()
        miso_pin = singletons.microcontrollerConfig.getMISOPin()
        dc_pin = singletons.microcontrollerConfig.getDisplayDCPin()
        reset_pin = singletons.microcontrollerConfig.getDisplayResetPin()

        self.enabled = True

        if self.enabled:
            try:
                spi = SPI(singletons.microcontrollerConfig.getSpi(), baudrate=10000000, sck=Pin(sck_pin), mosi=Pin(mosi_pin),
                          miso=Pin(miso_pin))
                self.d = Display(spi, cs=disp_cs, dc=Pin(dc_pin), rst=Pin(reset_pin))
                self.logger.info("Display found!")
                self.enabled = True

                self.font = XglcdFont('fonts/FixedFont5x8.c', 5, 8)

                sleep(1)

                self.d.clear()
                self.d.draw_line(217, 319, 217, 0, WHITE)
                self.setWlanConnected(False)
                self.setMqttConnected(False)
                create_task(self.update_uptime())
            except Exception as e:
                self.logger.error("Ein Fehler ist aufgetreten:", e)
                self.enabled = False


    async def update_uptime(self):
        if self.enabled:
            from utime import time
            _st = time()  # start time

            while True:
                uptime = time() - _st
                self.setUptime("Uptime: {}".format(uptime))
                await sleep_ms(10000)

    def setWlanConnected(self, wlanConnected: bool):
        if self.enabled:
            if wlanConnected is True:
                self.d.draw_text(220, SIZE_Y, 'WLAN', self.font, GREEN, landscape=True)
            else:
                self.d.draw_text(220, SIZE_Y, 'WLAN', self.font, RED, landscape=True)

    def setMqttConnected(self, mqttConnected: bool):
        if self.enabled:
            if mqttConnected is True:
                self.d.draw_text(230, SIZE_Y, 'MQTT', self.font, GREEN, landscape=True)
            else:
                self.d.draw_text(230, SIZE_Y, 'MQTT', self.font, RED, landscape=True)

    def setVersion(self, version: str):
        if self.enabled:
            self.d.fill_rectangle(220, 0, 9, 70, BLACK)
            self.d.draw_text(220, self.getYCoordinateRight(version, 5, 6), version, self.font, WHITE, landscape=True)

    def setAutoUpdate(self, autoUpdate: bool):
        if self.enabled:
            self.d.fill_rectangle(230, 0, 9, 70, BLACK)
            if autoUpdate is not False:
                self.d.draw_text(230, 26, 'Auto', self.font, WHITE, landscape=True)
            else:
                self.d.draw_text(230, 36, 'Manual', self.font, WHITE, landscape=True)

    def setIPAddress(self, ip: str):
        if self.enabled:
            self.d.fill_rectangle(230, 70, 9, 180, BLACK)
            self.d.draw_text(230, self.getYCoordinateCentered(ip, 5, 160), ip, self.font, WHITE, landscape=True)

    def setUptime(self, uptime: str):
        if self.enabled:
            self.d.fill_rectangle(220, 70, 9, 180, BLACK)
            self.d.draw_text(220, self.getYCoordinateCentered(uptime, 5, 160), uptime, self.font, WHITE, landscape=True)

    def getYCoordinateCentered(self, text: str, fontWidth: int, yRef: int) -> int:
        return int(yRef + len(text) * fontWidth / 2)

    def getYCoordinateRight(self, text: str, fontWidth: int, yRef: int) -> int:
        return int(yRef + len(text) * fontWidth)
