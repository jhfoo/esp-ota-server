from machine import Pin, SPI
import axp202c
import st7789

# global
tft = None
spi = None
axp = None

def main():
    global tft, spi, axp
    
    # try:
    # Turn power on display power
    axp = axp202c.PMU()
    axp.enablePower(axp202c.AXP202_LDO2)

    # initalize spi port
    spi = SPI(
        2,
        baudrate=32000000,
        polarity=1,
        phase=0,
        bits=8,
        firstbit=0,
        sck=Pin(18, Pin.OUT),
        mosi=Pin(19, Pin.OUT))

    # configure display
    tft = st7789.ST7789(
        spi, 240, 240,
        cs=Pin(5, Pin.OUT),
        dc=Pin(27, Pin.OUT),
        backlight=Pin(12, Pin.OUT),
        rotation=0)

    # enable display
    tft.init()
    tft.fill(st7789.BLACK)

    # finally:
    #     # shutdown spi
    #     spi.deinit()
    #     # turn off display power
    #     axp.disablePower(axp202c.AXP202_LDO2)

main()