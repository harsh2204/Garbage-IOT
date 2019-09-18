
# This file is executed on every boot (including wake-boot from deepsleep)
import os
import uos, machine
from machine import Pin, I2C
import ssd1306
import network
import dht


try:
  import usocket as socket
except:
  import socket


#import esp

#esp.osdebug(None)


#uos.dupterm(None, 1) # disable REPL on UART(0)

import gc

#import webrepl

#webrepl.start()

gc.collect()

ssid = 'Udey Gupta-2.4G'
password = 'utt1971sh'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())


i2c = I2C(-1, Pin(4), Pin(5))

oled = ssd1306.SSD1306_I2C(128, 32, i2c)

oled.fill(0)

oled.text('Garbage Boi', 0, 0)
oled.text('Loading Garbage', 0, 10)
oled.text('Info', 0, 20)

oled.show()

# Uncomment the following to run webserver on boot
#exec(open('./example.py').read(),globals())



