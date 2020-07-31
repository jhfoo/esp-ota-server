# std
import framebuf
import math

# 3rd party
from writer import CWriter

# custom 
import font6

SCR_WIDTH = 240
SCR_HEIGHT = 240

def _rgb565(red, green, blue):
    ret = 0
    blue5bit = math.floor(blue / 255 * 31)
    print (blue5bit)
    print ('blue {0:b}'.format(blue5bit))
    ret = blue5bit << 11

    red6bit = math.floor(red / 255 * 63)
    print (red6bit)
    print ('red {0:b}'.format(red6bit))
    ret = ret | (red6bit << 5)

    green5bit = math.floor(green / 255 * 31)
    print (green5bit)
    print ('green {0:b}'.format(green5bit))
    ret = ret | green5bit

    print ('packed {0:b}'.format(ret))
    return ret

class ST7789Buffer(framebuf.FrameBuffer):
    BLACK = _rgb565(0,0,0)
    WHITE = _rgb565(255,255,255)

    RED = _rgb565(255,0,0)
    GREEN = _rgb565(0,255,0)
    BLUE = _rgb565(0,0,255)

    CYAN = _rgb565(0,255,255)
    PURPLE = _rgb565(255,0,255)
    YELLOW = _rgb565(255,255,0)

    GRAY = _rgb565(64,64,64)

    def __init__(self):
        self.width = SCR_WIDTH
        self.height = SCR_HEIGHT
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.font = font6
        self.writer = CWriter(self, self.font, 0xffff, 0)

    def renderText(self, text, x, y, fgcolor=0xffff, bgcolor=0x0000):
        CWriter.set_textpos(self, y, x)
        self.writer.setcolor(fgcolor, bgcolor)
        self.writer.printstring(text)

    def show(self, driver):
        driver.blit_buffer(self, 0, 0, SCR_WIDTH, SCR_HEIGHT)

    @staticmethod
    def rgb565(red, green, blue):
        return _rgb565(red, green, blue)

