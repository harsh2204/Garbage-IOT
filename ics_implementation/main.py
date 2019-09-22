from gbg import get_garbage, get_garbage_cal, rtc
from time import sleep, sleep_ms
from machine import Timer, Pin
import machine

#USE THIS https://github.com/peterhinch/micropython-async/blob/master/DRIVERS.md

TIMEOUT = 5#s

R_PIN = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
new_click_detected = False

def callback(p):
    global new_click_detected
    new_click_detected = True
    

#pin.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=callback, hard=True)
R_PIN.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback, hard=True)


def draw_cal(texts, date):
  global oled
  date = date.split('-')
  oled.fill(0)
  longest = 0  
  for i in range(len(texts)):
    oled.text(texts[i], 0, i*10)  
    if len(texts[i]) > longest:
      longest = len(texts[i])
    oled.text(date[i], 128-(len(date[i])*8), i*10)
  oled.vline((longest+1)*8, 0, (longest+1)*8, 30)
  oled.show()
  
def timeout_callback(t):    
    global TIMEOUT
    if TIMEOUT < 0:
        oled.poweroff()
        #machine.deepsleep()
    else:
        TIMEOUT -= 1    
  
texts, date = get_garbage()

if date[0] == '9':
  texts.append("running dwnld")

  draw_cal(texts, date)
  get_garbage_cal()
  sleep(2)
  texts_new, date_new = get_garbage()
  draw_cal(texts_new, date_new)
else:
  draw_cal(texts, date)
  
  
  
tim = Timer(-1)
tim.init(period = 1000, mode=Timer.PERIODIC, callback=timeout_callback)

value = 0
while True:
    while not new_click_detected:
        pass

    sleep_ms(20)
    if R_PIN.value() == 0:
        
        TIMEOUT = 10
        oled.poweron()

    new_click_detected = False   
