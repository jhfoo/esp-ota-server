# std
from machine import Timer
import random

# 3rd party
import st7789
import axp202c


# custom
from lib.st7789buf import ST7789Buffer
from lib.TouchMgr import TouchMgr
from PowerApp import PowerApp
from NetworkApp import NetworkApp
# import lib.courier20 as courier20

AXP202_LOW = 2600
AXP202_MED = 2950
AXP202_HIGH = 3300

fbuf = ST7789Buffer(tft)
axp.setLDO2Voltage(AXP202_MED)
RefreshTimer = Timer(0)
tm = TouchMgr(touch, IsStopOnMatch = False, axp = axp)
power = PowerApp(axp = axp)
netapp = NetworkApp()

tft.fill(st7789.BLACK)
SCREEN_MAXY = 240
SCREEN_MAXX = 240
PADDING = 20
STARTY = 20
PAGE_POWER = 'POWER'
PAGE_NETWORK = 'NETWORK'
PAGE_ACCEL = 'ACCEL'
ACTIVE_PAGE = PAGE_POWER
SCREEN_OPT = {
    'StartY': 20,
    'LineHeight': 20,
    'LineFont': 'roboto18'
}

def renderAppBar():
    fbuf.line(0, STARTY - 1, SCREEN_MAXX, STARTY - 1, ST7789Buffer.WHITE)

def renderButtons():
    # fbuf.rect(0, SCREEN_MAXY - PADDING * 2, SCREEN_MAXX, PADDING * 2, ST7789Buffer.WHITE)
    fbuf.line(0, SCREEN_MAXY - PADDING * 2, SCREEN_MAXX, SCREEN_MAXY - PADDING * 2, ST7789Buffer.WHITE)
    fbuf.line(int(SCREEN_MAXX / 2), SCREEN_MAXY - PADDING * 2, int(SCREEN_MAXX / 2), SCREEN_MAXY, ST7789Buffer.WHITE)
    fbuf.renderText('Home', PADDING, SCREEN_MAXY - PADDING * 2 + 15, ST7789Buffer.WHITE)
    fbuf.renderText('Next', int(SCREEN_MAXX / 2 + PADDING + 30), SCREEN_MAXY - PADDING * 2 + 15, ST7789Buffer.WHITE)

def clearContentBuffer():
    fbuf.fill_rect(0, STARTY, SCREEN_MAXX, SCREEN_MAXY - PADDING * 2 - STARTY - 1, ST7789Buffer.BLACK)

def renderNetworkPage():
    print ('renderNetworkPage()')
    clearContentBuffer()
    netapp.renderPage(fbuf, ScreenOpt = SCREEN_OPT)


def renderPowerPage(time = None):
    clearContentBuffer()
    power.renderPage(fbuf, ScreenOpt = SCREEN_OPT)
    # print (tft)

def renderAccelPage():
    print ('renderAccelPage()')
    clearContentBuffer()
    fbuf.renderText('Accelerator', 10, STARTY, fgcolor=ST7789Buffer.WHITE, bgcolor=ST7789Buffer.BLACK, font='roboto18')
    fbuf.show()


def renderPage():
    if ACTIVE_PAGE == PAGE_POWER:
        renderPowerPage()
    elif ACTIVE_PAGE == PAGE_NETWORK:
        renderNetworkPage()
    elif ACTIVE_PAGE == PAGE_ACCEL:
        renderAccelPage()
        

def onLeftBtn():
    global ACTIVE_PAGE
    
    print ('onLeftBtn()')
    if ACTIVE_PAGE == PAGE_POWER:
        ACTIVE_PAGE = PAGE_NETWORK
    elif ACTIVE_PAGE == PAGE_NETWORK:
        ACTIVE_PAGE = PAGE_ACCEL
    elif ACTIVE_PAGE == PAGE_ACCEL:
        ACTIVE_PAGE = PAGE_POWER

    renderPage()

def onRightBtn():
    print ('onRightBtn()')
    tm.stop()

def start():
    fbuf.fill(0)
    renderAppBar()
    renderButtons()
    renderPowerPage()
    tm.addZone(0, SCREEN_MAXY - PADDING * 2, int(SCREEN_MAXX / 2), SCREEN_MAXY, onLeftBtn)
    tm.addZone(int(SCREEN_MAXX / 2), SCREEN_MAXY - PADDING * 2, SCREEN_MAXX, SCREEN_MAXY, onRightBtn)
    tm.start()
