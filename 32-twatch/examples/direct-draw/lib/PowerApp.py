from st7789buf import ST7789Buffer

class PowerApp():
    def __init__(self, axp):
        self.axp = axp

    def renderPage(self, buffer, ScreenOpt):
        LineY = ScreenOpt['StartY']

        buffer.renderText("Charging  : {}".format('YES' if self.axp.isChargeing() > 0 else 'NO'), 10, LineY, fgcolor=ST7789Buffer.RED, font=ScreenOpt['LineFont'])
        LineY += ScreenOpt['LineHeight']
        buffer.renderText("Temp      : {}C".format(self.axp.getTemp()), 10, LineY, fgcolor=ST7789Buffer.GREEN, font=ScreenOpt['LineFont'])
        LineY += ScreenOpt['LineHeight']

        buffer.renderText("Vbus Curr : {}mA".format(self.axp.getVbusCurrent()), 10, LineY, fgcolor=ST7789Buffer.BLUE, font=ScreenOpt['LineFont'])
        LineY += ScreenOpt['LineHeight']
        buffer.renderText("Vbus Volt : {}mV".format(self.axp.getVbusVoltage()), 10, LineY, fgcolor=ST7789Buffer.WHITE, font=ScreenOpt['LineFont'])
        LineY += ScreenOpt['LineHeight']
        
        # fbuf.renderText("AcIn Curr : {}mA".format(axp.getAcinCurrent()), 10, LineY, fgcolor=ST7789Buffer.YELLOW, font='roboto18')
        # LineY += LineHeight
        # fbuf.renderText("AcIn Volt : {}mV".format(axp.getAcinVoltage()), 10, LineY, fgcolor=ST7789Buffer.CYAN, font='roboto18')
        # LineY += LineHeight

        buffer.renderText("Batt CCurr: {}mA".format(self.axp.getBattChargeCurrent()), 10, LineY, fgcolor=ST7789Buffer.PURPLE, font=ScreenOpt['LineFont'])
        LineY += ScreenOpt['LineHeight']
        buffer.renderText("Batt DCurr: {}mA".format(self.axp.getBattDischargeCurrent()), 10, LineY, fgcolor=ST7789Buffer.WHITE, font=ScreenOpt['LineFont'])
        LineY += ScreenOpt['LineHeight']
        buffer.renderText("Batt Volt : {}mV".format(self.axp.getBattVoltage()), 10, LineY, fgcolor=ST7789Buffer.GRAY, font=ScreenOpt['LineFont'])
        LineY += ScreenOpt['LineHeight']
        buffer.renderText("Batt      : {}%".format(self.axp.getBattPercentage()), 10, LineY, fgcolor=ST7789Buffer.WHITE, font=ScreenOpt['LineFont'])

        buffer.show()
