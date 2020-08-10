# std
from machine import Timer
import random

# 3rd party
import st7789
import axp202c

# custom
from lib.st7789buf import ST7789Buffer
from lib.TouchMgr import TouchMgr
# import lib.courier20 as courier20

AXP202_LOW = 2600
AXP202_MED = 2950
AXP202_HIGH = 3300

fbuf = ST7789Buffer(tft)
axp.setLDO2Voltage(AXP202_MED)
RefreshTimer = Timer(0)
tm = TouchMgr(touch, IsStopOnMatch = False, axp = axp)

tft.fill(st7789.BLACK)
SCREEN_MAXY = 240
SCREEN_MAXX = 240
PADDING = 20
PAGE_POWER = 'POWER'
PAGE_NETWORK = 'NETWORK'
ACTIVE_PAGE = PAGE_POWER


def renderButtons():
    # fbuf.rect(0, SCREEN_MAXY - PADDING * 2, SCREEN_MAXX, PADDING * 2, ST7789Buffer.WHITE)
    fbuf.line(0, SCREEN_MAXY - PADDING * 2, SCREEN_MAXX, SCREEN_MAXY - PADDING * 2, ST7789Buffer.WHITE)
    fbuf.line(int(SCREEN_MAXX / 2), SCREEN_MAXY - PADDING * 2, int(SCREEN_MAXX / 2), SCREEN_MAXY, ST7789Buffer.WHITE)
    fbuf.renderText('Home', PADDING, SCREEN_MAXY - PADDING * 2 + 15, ST7789Buffer.WHITE)
    fbuf.renderText('Next', int(SCREEN_MAXX / 2 + PADDING + 30), SCREEN_MAXY - PADDING * 2 + 15, ST7789Buffer.WHITE)

def renderNetworkPage():
    print ('renderNetworkPage()')
    fbuf.fill_rect(0,0,SCREEN_MAXX, SCREEN_MAXY - PADDING * 2 - 1, ST7789Buffer.BLACK)
    fbuf.renderText('Roboto18', 10, 10, fgcolor=ST7789Buffer.WHITE, bgcolor=ST7789Buffer.BLACK, font='roboto18')
    fbuf.show()


def renderPowerPage(time = None):
    LineHeight = 20
    LineY = 10

    fbuf.fill_rect(0,0,SCREEN_MAXX, SCREEN_MAXY - PADDING * 2 - 1, ST7789Buffer.BLACK)
    # print (tft)
    fbuf.renderText("Charging  : {}".format('YES' if axp.isChargeing() > 0 else 'NO'), 10, LineY, fgcolor=ST7789Buffer.RED, font='roboto18')
    LineY += LineHeight
    fbuf.renderText("Temp      : {}C".format(axp.getTemp()), 10, LineY, fgcolor=ST7789Buffer.GREEN, font='roboto18')
    LineY += LineHeight

    fbuf.renderText("Vbus Curr : {}mA".format(axp.getVbusCurrent()), 10, LineY, fgcolor=ST7789Buffer.BLUE, font='roboto18')
    LineY += LineHeight
    fbuf.renderText("Vbus Volt : {}mV".format(axp.getVbusVoltage()), 10, LineY, fgcolor=ST7789Buffer.WHITE, font='roboto18')
    LineY += LineHeight
    
    # fbuf.renderText("AcIn Curr : {}mA".format(axp.getAcinCurrent()), 10, LineY, fgcolor=ST7789Buffer.YELLOW, font='roboto18')
    # LineY += LineHeight
    # fbuf.renderText("AcIn Volt : {}mV".format(axp.getAcinVoltage()), 10, LineY, fgcolor=ST7789Buffer.CYAN, font='roboto18')
    # LineY += LineHeight

    fbuf.renderText("Batt CCurr: {}mA".format(axp.getBattChargeCurrent()), 10, LineY, fgcolor=ST7789Buffer.PURPLE, font='roboto18')
    LineY += LineHeight
    fbuf.renderText("Batt DCurr: {}mA".format(axp.getBattDischargeCurrent()), 10, LineY, fgcolor=ST7789Buffer.WHITE, font='roboto18')
    LineY += LineHeight
    fbuf.renderText("Batt Volt : {}mV".format(axp.getBattVoltage()), 10, LineY, fgcolor=ST7789Buffer.GRAY, font='roboto18')
    LineY += LineHeight
    fbuf.renderText("Batt      : {}%".format(axp.getBattPercentage()), 10, LineY, fgcolor=ST7789Buffer.WHITE, font='roboto18')

    fbuf.show()

def renderPage():
    if ACTIVE_PAGE == PAGE_POWER:
        renderPowerPage()
    elif ACTIVE_PAGE == PAGE_NETWORK:
        renderNetworkPage()

def onLeftBtn():
    global ACTIVE_PAGE
    
    print ('onLeftBtn()')
    if ACTIVE_PAGE == PAGE_POWER:
        ACTIVE_PAGE = PAGE_NETWORK
    elif ACTIVE_PAGE == PAGE_NETWORK:
        ACTIVE_PAGE = PAGE_POWER

    renderPage()

def onRightBtn():
    print ('onRightBtn()')
    tm.stop()

def onRefreshTimer2(tim = None):
    global fbuf
    fbuf.fill(0)
    fbuf.text('MicroPython!', random.randint(10, 100), random.randint(10, 100), 0xffff)

    fbuf.renderText('Woohoo!', random.randint(10, 100), random.randint(10, 100), 0xF800)
    fbuf.renderText('Woohoo!', random.randint(10, 100), random.randint(10, 100), 0xF800)

    fbuf.show()

fbuf.fill(0)
renderButtons()
renderPowerPage()
tm.addZone(0, SCREEN_MAXY - PADDING * 2, int(SCREEN_MAXX / 2), SCREEN_MAXY, onLeftBtn)
tm.addZone(int(SCREEN_MAXX / 2), SCREEN_MAXY - PADDING * 2, SCREEN_MAXX, SCREEN_MAXY, onRightBtn)
tm.start()
