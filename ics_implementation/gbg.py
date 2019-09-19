
# garbage.py
import urequests
import ntptime
import machine
import os
import ujson

rtc = machine.RTC()

def get_date():
  ntptime.host = 'ca.pool.ntp.org'
  ntptime.settime()
  return "-".join([str(x) for x in rtc.datetime()[:3]])

def get_garbage_cal(): #In the end we can trigger this through a hidden button press
  endpoint = 'https://recollect.a.ssl.fastly.net/api/places/A40195C4-6C71-11E9-994E-10946165592B/services/1063/events.en.ics'
  
  if 'cal.json' in os.listdir('.'):
    os.remove('cal.json')
  
  res = urequests.get(endpoint)
  print(len(res.content))
  with open('cal.ics', 'wb') as f:
    f.write(res.content)
  
  
def get_desc_items(desc):
  evs = desc.split(', ')
  if len(evs) > 2:
      evs[-1] = evs[-1].split('and ')[-1]
  else:
      evs = desc.split(' and ') 
  return evs  


def set_events():
  events = {}
  if 'cal.ics' not in os.listdir('.'):
    print("Please download the calendar before running a query")
    return None
  with open('cal.ics', 'r') as f:    
    data = f.read().split('\n')
    i = 0
    while i < len(data):      
      if data[i][:11] == 'DESCRIPTION':
        desc = data[i].split(':')[-1].replace('\\', '').strip()
        
        i = i + 1
        date = data[i].split('DATE:')[-1].strip()
        date = [date[:4] , date[4:6], date[-2:]]
        if desc not in events:
          events[desc] = [date]
        else:
          events[desc].append(date)
      i = i + 1
    # return events
    with open('cal.json', 'w') as outf:
      s = ujson.dumps(events)
      outf.write(s)
  

def get_events():
  if 'cal.json' not in os.listdir('.'): #Assumes cal.ics is in the directory
    print('cal.json not found')
    set_events()
  with open('cal.json', 'r') as f:
    print('Loading local cache events')
    return ujson.loads(f.read())


def get_garbage():
  now = [int(x) for x in get_date().split('-')]
  evs = get_events()
  if evs == None:
    return (["Calendar", "now found"], '9999-99-99')
  closest = 31
  dates = []
  for desc, dlist in evs.items():
    for date in dlist:      
      if (int(date[0]) - now[0]) >= 0:
        if int(date[1]) == now[1] and int(date[2]) >= now[2] and int(date[2])-now[2] < closest: # change the last >= to > if ignore today's date
          info = get_desc_items(desc)
          
          for i in range(len(info)):         
            if info[i] == 'garbage exemption day':            
              info[i] = 'grbg exmp'
            if info[i] == 'battery pickup day':
              info[i] = 'battery pkp'
          
          ndate = "-".join(date)
          dates.append((info, ndate))
      else:
        dates = [(["Calendar out", "of date."], '9669-69-69')]
          #stupid idea but fixable
          #else:            
          #  for ch in ['a', 'e', 'i', 'o', 'u']:
          #    if ch in info[i]:
          #      info[i] = info[i].replace(ch, "")
          #  print(info[i])
            
  return dates[-1]

