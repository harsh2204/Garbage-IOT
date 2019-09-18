from icalendar import Calendar, Event
from pprint import pprint
events = {}

with open('events.en.ics', 'r') as f:
    cal = Calendar.from_ical(f.read())
    for component in cal.walk():
        if component.name == "VEVENT":
            evs = []
            desc = str(component.get('description'))
            
            evs = desc.split(', ')

            if len(evs) > 2:
                evs[-1] = evs[-1].split('and ')[-1]
            else:
                evs = desc.split(' and ') 
            events.append({component.get('dtstart').dt : evs})

pprint(events)

