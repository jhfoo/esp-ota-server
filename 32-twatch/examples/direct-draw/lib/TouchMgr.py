from machine import Timer
import axp202c
import math

class TouchMgr():
    def __init__(self, driver, TimerId = 3, IsRotate = True, IsStopOnMatch = True, TimerInterval = 100, axp = None, IdleTimeout = 10 * 1000):
        self.ScreenWidth = 240
        self.ScreenHeight = 240
        self.IdleTimeout = IdleTimeout
        self.IdleCounter = 0
        self.TouchDriver = driver
        self.timer = Timer(TimerId)
        self.TimerInterval = TimerInterval
        self.zones = []
        self.IsStopOnMatch = IsStopOnMatch
        self.IsRotate = IsRotate
        self.axp = axp
        self.LastX = None
        self.LastY = None
        self.StartX = None
        self.StartY = None
        self.LastTouchZone = None
        self.StopMonitor = False
        self.IsScreenPowerOn = True
        # super().__init__(self.buffer)

    def addZone(self, x1, y1, x2, y2, cb):
        self.zones.append({
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'cb': cb
        })

    def start(self):
        self.StopMonitor = False
        self.LastTouchZone = None
        self.timer.init(period=self.TimerInterval, mode=Timer.ONE_SHOT, callback=self.testTouch)

    def getTouchedZone(self, TestX, TestY):
        for zone in self.zones:
            if (TestX >= zone['x1'] and TestY >= zone['y1']
                and TestX <= zone['x2'] and TestY <= zone['y2']):
                return zone

    def testTouch(self, timer):
        # print('testTouch()')
        if self.TouchDriver.touched:
            print ('Counter: {}, Timeout: {}'.format(self.IdleCounter, self.IdleTimeout))
            if self.IdleCounter >= self.IdleTimeout:
                print ('Turn on screen')
                if self.IsScreenPowerOn == False:
                    self.IsScreenPowerOn = True
                    self.axp.enablePower(axp202c.AXP202_LDO2)
            self.IdleCounter = 0

            if self.StartX == None:
                self.StartX = self.TouchDriver.touches[0]['x']
                self.StartY = self.TouchDriver.touches[0]['y']

            if self.IsRotate == True:
                FinalX = self.ScreenWidth - self.TouchDriver.touches[0]['x']
                FinalY = self.ScreenHeight - self.TouchDriver.touches[0]['y']
            else:
                FinalX = self.TouchDriver.touches[0]['x']
                FinalY = self.TouchDriver.touches[0]['y']

            if FinalX != self.LastX or FinalY != self.LastY:
                # debounce same coord
                self.LastX = FinalX
                self.LastY = FinalY
                self.LastTouchZone = self.getTouchedZone(FinalX, FinalY)
        else:
            # callback when touch released
            if self.LastTouchZone != None:
                if self.IsStopOnMatch == True:
                    print ('Stopped')
                    self.StopMonitor = True

                self.LastTouchZone['cb']()
                self.LastTouchZone = None
            elif self.StartX != None:
                # simple gesture detection
                # a gesture must exceed X distance
                width = self.StartX - self.TouchDriver.touches[0]['x']
                height = self.StartY - self.TouchDriver.touches[0]['y']
                distance = math.sqrt(width ** 2 + height ** 2)

                if abs(width) > abs(height):
                    if distance > 60:
                        if width > 0:
                            print ('Swipe right')
                        else:
                            print ('Swipe left')
                else:
                    if distance > 30:
                        if height > 0:
                            print ('Swipe bottom')
                        else:
                            print ('Swipe top')

                print ('From {}, {} to {}, {}: width = {}, height = {}'.format(self.StartX, self.StartY, self.LastX, self.LastY, width, height))
                print ('Distance: {}'.format(math.floor(distance)))

                self.StartX = None
                self.StartY = None
            else:
                # nothing happened
                if self.IdleCounter < self.IdleTimeout:
                    # timeout not reached
                    self.IdleCounter += self.TimerInterval
                else:
                    # timeout reached
                    self.StopMonitor = False
                    if self.IsScreenPowerOn == True:
                        self.IsScreenPowerOn = False
                        print ('Touch timeout')
                        self.axp.disablePower(axp202c.AXP202_LDO2)
                # print ('{}, {}'.format(self.IdleCounter, self.IdleTimeout))

        if self.StopMonitor == False:
            self.timer.init(period=self.TimerInterval, mode=Timer.ONE_SHOT, callback=self.testTouch)

    def stop(self):
        self.StopMonitor = True