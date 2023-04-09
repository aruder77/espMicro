from machine import Pin, SPI
from micropython import const
from uasyncio import sleep

from esp_micro.logutil import get_logger
from ili9341 import Display, color565
from xglcd_font import XglcdFont
from xpt2046 import Touch

YELLOW = const(0XFFE0)  # (255, 255, 0)

class DisplayController:

    def __init__(self):
        self.logger = get_logger()
        self.logger.info("initializing display...")

        dispCS = Pin(17, Pin.OUT)  # display shares spi
        dispCS.value(1)
        led = Pin(12, Pin.OUT)
        led.value(1)

        spi = SPI(0, baudrate=10000000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))

        d = Display(spi, cs=dispCS, dc=Pin(21), rst=Pin(20))
        d.clear(color565(64, 0, 255))
        font = XglcdFont('fonts/FixedFont5x8.c', 5, 8)
        sleep(1)
        d.clear()
        # d.draw_text(0, 319, 'Hello', font, color565(255, 0, 255), landscape=True)
        d.draw_text(0, 319, 'Hello', font, YELLOW, landscape=True)
