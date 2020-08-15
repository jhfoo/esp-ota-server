from st7789buf import ST7789Buffer

class NetworkApp():
    def __init__(self):
        print ('Init')

    def renderPage(self, buffer, ScreenOpt):
        LineY = ScreenOpt['StartY']

        buffer.renderText('Network', 10, LineY, fgcolor=ST7789Buffer.WHITE, bgcolor=ST7789Buffer.BLACK, font=ScreenOpt['LineFont'])
        LineY += ScreenOpt['LineHeight']

        buffer.show()
