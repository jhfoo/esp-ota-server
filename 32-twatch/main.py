import st7789
import axp202c
from machine import Timer
import framebuf
import random

from st7789buf import ST7789Buffer

fbuf = ST7789Buffer()
axp.setLDO2Voltage(1800)
RefreshTimer = Timer(0)

tft.fill(st7789.BLACK)

def onRefreshTimer(tim = None):
    print (axp.isBatteryConnect())
    print (axp.isChargeing())
    LineHeight = 15
    LineY = 10

    # print (tft)
    fbuf.renderText("Chargingg  : {}".format('YES' if axp.isChargeing() > 0 else 'NO'), 10, LineY, st7789.YELLOW, st7789.BLACK)
    LineY += LineHeight
    fbuf.renderText("Temp      : {}C".format(axp.getTemp()), 10, LineY, st7789.YELLOW, st7789.BLACK)
    LineY += LineHeight

    fbuf.renderText("Vbus Curr : {}mA".format(axp.getVbusCurrent()), 10, LineY, st7789.YELLOW, st7789.BLACK)
    LineY += LineHeight
    fbuf.renderText("Vbus Volt : {}mV".format(axp.getVbusVoltage()), 10, LineY, st7789.YELLOW, st7789.BLACK)
    LineY += LineHeight
    
    fbuf.renderText("AcIn Curr : {}mA".format(axp.getAcinCurrent()), 10, LineY, st7789.YELLOW, st7789.BLACK)
    LineY += LineHeight
    fbuf.renderText("AcIn Volt : {}mV".format(axp.getAcinVoltage()), 10, LineY, st7789.YELLOW, st7789.BLACK)
    LineY += LineHeight

    fbuf.renderText("Batt CCurr: {}mA".format(axp.getBattChargeCurrent()), 10, LineY, st7789.YELLOW, st7789.BLACK)
    LineY += LineHeight
    fbuf.renderText("Batt DCurr: {}mA".format(axp.getBattDischargeCurrent()), 10, LineY, st7789.YELLOW, st7789.BLACK)
    LineY += LineHeight
    fbuf.renderText("Batt Volt : {}mV".format(axp.getBattVoltage()), 10, LineY, st7789.YELLOW, st7789.BLACK)
    LineY += LineHeight
    fbuf.renderText("Batt      : {}%".format(axp.getBattPercentage()), 10, LineY, st7789.YELLOW, st7789.BLACK)
    fbuf.show(tft)
    # RefreshTimer.init(period=2000, mode=Timer.ONE_SHOT, callback=onRefreshTimer)

def onRefreshTimer2(tim = None):
    global fbuf
    fbuf.fill(0)
    fbuf.text('MicroPython!', random.randint(10, 100), random.randint(10, 100), 0xffff)

    fbuf.renderText('Woohoo!', random.randint(10, 100), random.randint(10, 100), 0xF800)
    fbuf.renderText('Woohoo!', random.randint(10, 100), random.randint(10, 100), 0xF800)

    fbuf.show(tft)


onRefreshTimer()
