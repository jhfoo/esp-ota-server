from machine import SPI, Pin
import st7789
import vga2_bold_16x32 as font
import random

print ('Booting')
spi = SPI(2, baudrate=30000000, polarity=1, phase=1, sck=Pin(18), mosi=Pin(19))
#machine.SPI(2, baudrate=40000000, polarity=1, sck=machine.Pin(18), mosi=machine.Pin(19))
display = st7789.ST7789(
    spi,
    240, 240,
    reset=Pin(23, Pin.OUT),
    cs=Pin(5, Pin.OUT),
    dc=Pin(27, Pin.OUT),
    backlight=Pin(12, Pin.OUT),
    rotation=0)
display.init()
display.fill(st7789.color565(5,5,5))
display.text(font, 'KungFOO rocks!', 50,50,
    st7789.color565(
        random.getrandbits(8),
        random.getrandbits(8),
        random.getrandbits(8)),
    st7789.color565(
        random.getrandbits(8),
        random.getrandbits(8),
        random.getrandbits(8))
    )

