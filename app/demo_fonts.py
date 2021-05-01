"""ILI9341 demo (fonts)."""
from time import sleep
from ili9341 import Display, color565
from machine import Pin, SPI
from xglcd_font import XglcdFont


def test():
    """Test code."""
    spi = SPI(2, baudrate=27000000, sck=Pin(19), mosi=Pin(23))
    display = Display(spi, dc=Pin(21), cs=Pin(22), rst=Pin(18))
    Pin(5, Pin.OUT, value=0)

    print('Loading fonts...')
    print('Loading arcadepix')
    arcadepix = XglcdFont('fonts/ArcadePix9x11.c', 9, 11)
    print('Loading bally')
    bally = XglcdFont('fonts/Bally7x9.c', 7, 9)
    print('Loading broadway')
    broadway = XglcdFont('fonts/Broadway17x15.c', 17, 15)
    print('Loading espresso_dolce')
    espresso_dolce = XglcdFont('fonts/EspressoDolce18x24.c', 18, 24)
    print('Loading fixed_font')
    fixed_font = XglcdFont('fonts/FixedFont5x8.c', 5, 8)
    print('Loading neato')
    neato = XglcdFont('fonts/Neato5x7.c', 5, 7, letter_count=223)
    print('Loading robotron')
    robotron = XglcdFont('fonts/Robotron13x21.c', 13, 21)
    print('Loading unispace')
    unispace = XglcdFont('fonts/Unispace12x24.c', 12, 24)
    print('Loading wendy')
    wendy = XglcdFont('fonts/Wendy7x8.c', 7, 8)
    print('Fonts loaded.')

    display.draw_text(0, 0, 'Arcade Pix 9x11', arcadepix, color565(255, 0, 0))
    display.draw_text(0, 22, 'Bally 7x9', bally, color565(0, 255, 0))
    display.draw_text(0, 43, 'Broadway 17x15', broadway, color565(0, 0, 255))
    display.draw_text(0, 66, 'Espresso Dolce 18x24', espresso_dolce,
                      color565(0, 255, 255))
    display.draw_text(0, 104, 'Fixed Font 5x8', fixed_font,
                      color565(255, 0, 255))
    display.draw_text(0, 125, 'Neato 5x7', neato, color565(255, 255, 0))
    display.draw_text(0, 155, 'ROBOTRON 13X21', robotron,
                      color565(255, 255, 255))
    display.draw_text(0, 190, 'Unispace 12x24', unispace,
                      color565(255, 128, 0))
    display.draw_text(0, 220, 'Wendy 7x8', wendy, color565(255, 0, 128))

