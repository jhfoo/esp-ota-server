import machine
from machine import Pin, Timer
import ssd1306
import font6
from writer import Writer
import dht
import util

OLED_WIDTH = 128
OLED_HEIGHT = 64
PinScl = Pin(14)
PinSda = Pin(2)
PinBoot = Pin(0)
PinLed = Pin(4)
BattLevel = 0

def page2(tim):
    tim.deinit()
    oled.fill(0)

    Writer.set_textpos(oled, 15, 0)
    wrtr.printstring("Line 2y")
    Writer.set_textpos(oled, 30, 0)
    wrtr.printstring("Line 3y")
    Writer.set_textpos(oled, 45, 0)
    wrtr.printstring("Line 4y")
    oled.show()
    tim.init(period=3 * 1000, mode=Timer.ONE_SHOT, callback=page3)
    
def page3(tim):
    oled.poweroff()
    tim.init(period=3 * 1000, mode=Timer.ONE_SHOT, callback=page4)

def page4(tim):
    global oled
    oled.poweron()
    tim.init(period=3 * 1000, mode=Timer.ONE_SHOT, callback=page5)
    # tim.init(period=3 * 1000, mode=Timer.ONE_SHOT, callback=page4)

def page5(tim):
    oled.invert(1)
    tim.init(period=3 * 1000, mode=Timer.ONE_SHOT, callback=page6)

def page6(tim):
    oled.poweroff()

def BatteryPage(tim):
    global BattLevel
    oled.fill(0)
    icon = util.loadImage('icons/battery' + str(BattLevel) + '4.pbm')
    oled.blit(icon, 100,0)
    oled.show()
    if (BattLevel < 4):
        BattLevel += 1
        tim.init(period=1 * 1000, mode=Timer.ONE_SHOT, callback=BatteryPage)
    else:
        tim.init(period=1 * 1000, mode=Timer.ONE_SHOT, callback=page2)

def DhtPage(tim):
    oled.fill(0)
    # d = dht.DHT11(machine.Pin(5))
    d = dht.DHT22(machine.Pin(5))
    d.measure()
    Writer.set_textpos(oled, 15, 0)
    wrtr.printstring("Temp")

    Writer.set_textpos(oled, 15, 80)
    wrtr.printstring(str(d.temperature()) + "C")

    Writer.set_textpos(oled, 30, 0)
    wrtr.printstring("Humi")

    Writer.set_textpos(oled, 30, 80)
    wrtr.printstring(str(d.humidity()) + "%")
    oled.show()
    tim.init(period=2 * 1000, mode=Timer.ONE_SHOT, callback=BatteryPage)

# i2c = machine.I2C(-1, PinScl, PinSda)
# print ('')
# print (i2c.scan())
# oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)
# wrtr = Writer(oled, font6)
# Writer.set_textpos(oled, 0, 0)
# wrtr.printstring("Hello World!")
# oled.show()
# tim = Timer(-1)
# tim.init(period=2 * 1000, mode=Timer.ONE_SHOT, callback=DhtPage)
