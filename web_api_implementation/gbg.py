# garbage.py
import urequests
import ujson
import ntptime
import machine
import gc

rtc = machine.RTC()

def get_date():
  ntptime.host = 'ca.pool.ntp.org'
  ntptime.settime()
  return "-".join([str(x) for x in rtc.datetime()[:3]])
 
def get_before_date(timedelta=7):

  date = list(rtc.datetime()[:3])
  target = date[-1] + timedelta
  if target < 28:
    date[-1] = date[-1] + timedelta
  else:
    date[-2] += 1
    date[-1] = abs(28 - target)
    if date[-2] >12:
      date[0] += 1
      date[-2] = 1
  print(date)
  return "-".join([str(x) for x in date])
  
def get_garbage():
  endpoint = 'https://api.recollect.net/api/places/A40195C4-6C71-11E9-994E-10946165592B/services/1063/events'
  params = {"nomerge": "0",
            "hide": "reminder_only",
            "after": get_date(),
            "before": get_before_date(),
            "locale": "en"}
  s = ""
  for k,v in params.items():
    s += k + "=" + v + "&"
  endpoint = endpoint+"/?"+s[:-1]
  print(endpoint)
  res = urequests.get(endpoint)
  print(len(res.content))
  data = ujson.loads(res.content.decode('utf-8'))
  res = None
  gc.collect()

  
  gbg = {}
  for e in data['events']:
    print(e['day'])
    evs = []
    for f in e['flags']:
      print(f['name'])
      evs.append(f['name'])
    gbg[e['day']] = evs
  data = None
  gc.collect()
  return gbg