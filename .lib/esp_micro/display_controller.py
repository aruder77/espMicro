from machine import Pin, SPI
from micropython import const
from uasyncio import sleep, sleep_ms, create_task

from esp_micro.logutil import get_logger
from homie.device import await_ready_state
from ili9341 import Display, color565
from xglcd_font import XglcdFont
from xpt2046 import Touch

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

        dispCS = Pin(17, Pin.OUT)  # display shares spi
        dispCS.value(1)
        led = Pin(12, Pin.OUT)
        led.value(1)

        spi = SPI(0, baudrate=10000000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
        self.d = Display(spi, cs=dispCS, dc=Pin(21), rst=Pin(20))
        self.font = XglcdFont('fonts/FixedFont5x8.c', 5, 8)

        sleep(1)
        self.d.clear()

        self.d.draw_line(217, 319, 217, 0, WHITE)

        self.setWlanConnected(False)
        self.setMqttConnected(False)

        create_task(self.update_uptime())

    async def update_uptime(self):
        from utime import time
        _st = time()  # start time

        while True:
            uptime = time() - _st
            self.setUptime("Uptime: {}".format(uptime))
            await sleep_ms(10000)


    def setWlanConnected(self, wlanConnected: bool):
        if wlanConnected is True:
            print("setting wlan!")
            self.d.draw_text(220, SIZE_Y, 'WLAN', self.font, GREEN, landscape=True)
        else:
            self.d.draw_text(220, SIZE_Y, 'WLAN', self.font, RED, landscape=True)

    def setMqttConnected(self, mqttConnected: bool):
        if mqttConnected is True:
            self.d.draw_text(230, SIZE_Y, 'MQTT', self.font, GREEN, landscape=True)
        else:
            self.d.draw_text(230, SIZE_Y, 'MQTT', self.font, RED, landscape=True)

    def setVersion(self, version: str):
        self.d.fill_rectangle(220, 0, 9, 70, BLACK)
        self.d.draw_text(220, self.getYCoordinateRight(version, 5, 6), version, self.font, WHITE, landscape=True)

    def setAutoUpdate(self, autoUpdate: bool):
        self.d.fill_rectangle(230, 0, 9, 70, BLACK)
        if autoUpdate is not False:
            self.d.draw_text(230, 26, 'Auto', self.font, WHITE, landscape=True)
        else:
            self.d.draw_text(230, 36, 'Manual', self.font, WHITE, landscape=True)

    def setIPAddress(self, ip: str):
        self.d.fill_rectangle(230, 70, 9, 180, BLACK)
        self.d.draw_text(230, self.getYCoordinateCentered(ip, 5, 160), ip, self.font, WHITE, landscape=True)

    def setUptime(self, uptime: str):
        self.d.fill_rectangle(220, 70, 9, 180, BLACK)
        self.d.draw_text(220, self.getYCoordinateCentered(uptime, 5, 160), uptime, self.font, WHITE, landscape=True)

    def getYCoordinateCentered(self, text: str, fontWidth: int, yRef: int) -> int:
        return int(yRef + len(text) * fontWidth / 2)

    def getYCoordinateRight(self, text: str, fontWidth: int, yRef: int) -> int:
        return int(yRef + len(text) * fontWidth)
