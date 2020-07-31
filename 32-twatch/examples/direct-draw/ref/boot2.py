# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import axp202
from machine import I2C, Pin, SPI
import st7789 as st7789

# custom modules
import coreboot.wifi

coreboot.wifi.autoInit()

# i2c = I2C(scl=Pin(22), sda=Pin(21))
power = axp202.PMU(sda=21,scl=22,intr=35)
power.enablePower(axp202.AXP202_LDO2)
print('Batt charge:    {}%'.format(power.getBattPercentage()))
print('Batt voltage:   {}mV'.format(power.getBattVoltage()))
print('Batt charge:    {}mA'.format(power.getBattChargeCurrent()))
print('Batt discharge: {}mA'.format(power.getBattDischargeCurrent()))
print('Batt input:     {}mW'.format(power.getBattInpower()))

# spi = SPI(1, baudrate=30000000, polarity=1, sck=Pin(18), mosi=Pin(19))
# # spi = SPI(2, baudrate=30000000, polarity=1)
# tft = st7789.ST7789(
#     spi,
#     240, 240,
#     reset=Pin(23, Pin.OUT),
#     cs=Pin(5, Pin.OUT),
#     dc=Pin(27, Pin.OUT),
#     backlight=Pin(12, Pin.OUT)
#     # xstart=240,
#     # ystart=240
#     )
# tft.init()
# # tft.fill(st7789.BLUE)
# tft.pixel(0,0,st7789.YELLOW)
# tft.pixel(0,239,st7789.YELLOW)
# tft.pixel(239,239,st7789.YELLOW)
# tft.pixel(239,0,st7789.YELLOW)
