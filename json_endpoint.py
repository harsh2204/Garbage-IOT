import requests
from pprint import pprint
from datetime import datetime, timedelta

endpoint = 'https://api.recollect.net/api/places/A40195C4-6C71-11E9-994E-10946165592B/services/1063/events'

params = {"nomerge": "1",
          "hide": "reminder_only",
          "after": datetime.today().strftime('%Y-%m-%d'),
          "before": (datetime.today() + timedelta(weeks=2)).strftime('%Y-%m-%d'),
          "locale": "fr"}

res = requests.get(endpoint, params=params)

events = res.json()['events']

days = {}

for ev in events:
    # print(ev['day'])
    if 'flags' not in ev:
        days[ev['day']] = [ev['title']]
        continue
    if ev['day'] not in days:
        days[ev['day']] = [ev['flags'][0]['name']]
    else:
        days[ev['day']].append(ev['flags'][0]['name'])

pprint(days)