import gbg

events = gbg.get_garbage()
texts = list(events.values())[0]

date = list(events.keys())[0].split('-')
print(date)

oled.fill(0)
longest = 0
for i in range(len(texts)):
  oled.text(texts[i], 0, i*10)
  if len(texts[i]) > longest:
    longest = len(texts[i])
  oled.text(date[i], 128-(len(date[i])*8), i*10)
oled.vline((longest+1)*8, 0, (longest+1)*8, 30)
oled.show()
