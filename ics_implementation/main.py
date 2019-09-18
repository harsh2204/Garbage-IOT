from gbg import get_garbage, get_garbage_cal
from time import sleep


def draw_cal(texts, date):
  global oled
  date = date.split('-')
  oled.fill(0)
  longest = 0
  print(texts,date)
  for i in range(len(texts)):
    oled.text(texts[i], 0, i*10)  
    if len(texts[i]) > longest:
      longest = len(texts[i])
    oled.text(date[i], 128-(len(date[i])*8), i*10)
  oled.vline((longest+1)*8, 0, (longest+1)*8, 30)
  oled.show()
  
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
  
    