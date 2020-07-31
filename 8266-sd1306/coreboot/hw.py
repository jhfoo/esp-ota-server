# std imports
import machine
import ssd1306

# custom imports
import coreboot.constants as constants

Ssd1306 = None
isSsd1306Mounted = False
i2c = machine.I2C(-1, machine.Pin(constants.PIN_SCL), machine.Pin(constants.PIN_SDA))

def testSsd1306Mounted():
    global isSsd1306Mounted
    isSsd1306Mounted = 60 in i2c.scan()
    return isSsd1306Mounted

def init():
    global Ssd1306
    testSsd1306Mounted()
    if (isSsd1306Mounted):
        Ssd1306 = ssd1306.SSD1306_I2C(constants.OLED_WIDTH, constants.OLED_HEIGHT, i2c)
        Ssd1306.poweroff()