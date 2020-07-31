# std imports
import machine
import os
import math
import json
import network
import struct

# 3P modules
import coreboot.font6 as font6
from coreboot.writer import Writer

# custom imports
import coreboot.constants as constants
import coreboot.hw as hw

def isFileExist(filename):
  try:
    f = open(filename, "r")
    f.close()
    return True
  except OSError:  # open failed
    return False

def startApMode():
  print ('Starting wifi in ACCESS POINT mode')
  print ('*** TO BE IMPLEMENTED ***')

def startStationMode(opt):
  print ('Starting wifi in STATION mode')
  try:
    Infile = open(constants.FILE_CONFIG,'r')
    WifiConfig = json.loads(Infile.read())
    Infile.close()
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print ('Connecting to {}...'.format(WifiConfig['ssid']))
    wlan.connect(WifiConfig["ssid"], WifiConfig["pwd"])
    led = machine.Pin(constants.PIN_LED, machine.Pin.OUT)
    led.off()
    while not wlan.isconnected():
      pass
    led.on()
    print ('Connected to {}'.format(WifiConfig['ssid']))

    if ('DispWifiIp' in opt):
      if ('isSsd1306Mounted' in opt):
        hw.Ssd1306.poweron()
        y = 16
        IncrementY = 12
        hw.Ssd1306.text(WifiConfig['ssid'],0,0)
        hw.Ssd1306.text('I {}'.format(wlan.ifconfig()[0]),0,y)
        y += IncrementY
        hw.Ssd1306.text('M {}'.format(wlan.ifconfig()[1]),0,y)
        y += IncrementY
        hw.Ssd1306.text('G {}'.format(wlan.ifconfig()[2]),0,y)
        y += IncrementY
        hw.Ssd1306.text('D {}'.format(wlan.ifconfig()[3]),0,y)
        hw.Ssd1306.show()

        ScreenOffTimer = machine.Timer(-1)
        ScreenOffTimer.init(period=3000, mode=machine.Timer.ONE_SHOT, callback=lambda t:hw.Ssd1306.poweroff())

    print ('''
IP address :          {}
Netmask:              {}
Gateway:              {}
DNS:                  {}
    '''.format(wlan.ifconfig()[0], wlan.ifconfig()[1],
    wlan.ifconfig()[2],wlan.ifconfig()[3]))

  except Exception as err:
    print (err)

def registerDevice():
  print ('Registering device ')

def run(opt = {'DispWifiIp': True}):
  hw.init()
  stat = os.statvfs('')
  IsWifiConfigExist = isFileExist(constants.FILE_CONFIG)
  wlan = network.WLAN(network.STA_IF)
  MacAsStr = "%02x:%02x:%02x:%02x:%02x:%02x" % struct.unpack("BBBBBB",wlan.config('mac'))
  opt['isSsd1306Mounted'] = hw.isSsd1306Mounted
  
  print ('''
********************************************
  KungFoo's ESP8266 COREBOOT Runtime {}
********************************************
Block size (bytes):   {}
Filesystem size (KB): {}
Available (KB):       {} ({} %)

Wifi config:          {}
Wifi MAC:             {}

Detect SSD1306:       {}
  '''.format('v' + str(constants.VERSION_MAJOR) + '.' + str(constants.VERSION_MINOR),
  stat[0], stat[2],
  stat[3], math.floor(stat[3] * 100 / stat[2]),
  str(IsWifiConfigExist), MacAsStr,
  opt['isSsd1306Mounted']
  ))

  if (IsWifiConfigExist):
    startStationMode(opt)
  else:
    startApMode()
    registerDevice()

