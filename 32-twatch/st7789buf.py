# std
import framebuf

# 3rd party
from writer import CWriter

# custom 
import font6

SCR_WIDTH = 240
SCR_HEIGHT = 240

class ST7789Buffer(framebuf.FrameBuffer):
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