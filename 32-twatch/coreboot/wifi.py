# std imports
import machine
import os
import math
import json
import network
import struct

# custom imports
import coreboot.constants as constants

# module variables
wlan = None

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

def startStationMode():
  global wlan
  print ('Starting wifi in STATION mode')
  wlan = network.WLAN(network.STA_IF)
  try:
    Infile = open(constants.FILE_CONFIG,'r')
    WifiConfig = json.loads(Infile.read())
    Infile.close()
    
    wlan.active(True)
    print ('Connecting to {}...'.format(WifiConfig['ssid']))
    wlan.connect(WifiConfig["ssid"], WifiConfig["pwd"])
    # led = machine.Pin(constants.PIN_LED, machine.Pin.OUT)
    # led.off()
    while not wlan.isconnected():
      pass
    # led.on()
    print ('Connected to {}'.format(WifiConfig['ssid']))

    print ('''
IP address :          {}
Netmask:              {}
Gateway:              {}
DNS:                  {}
    '''.format(wlan.ifconfig()[0], wlan.ifconfig()[1],
    wlan.ifconfig()[2],wlan.ifconfig()[3]))

  except Exception as err:
    print (err)

def autoInit():
  global wlan
  isWifiConfig = isFileExist(constants.FILE_CONFIG)
  if (isWifiConfig):
    # ROADMAP: parse config to confirm STA mode
    startStationMode()
  else:
    startApMode()

  MacAsStr = "%02x:%02x:%02x:%02x:%02x:%02x" % struct.unpack("BBBBBB",wlan.config('mac'))

  print ('''
Wifi config:          {}
Wifi MAC:             {}
    '''.format(isWifiConfig, MacAsStr))




