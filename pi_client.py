#!/usr/local/env python
from evdev import InputDevice, categorize, ecodes
import json
import requests
import sys
import datetime;

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()

        return super(DateTimeEncoder, self).default(obj)

decode_dict = {2:"1", 3:"2", 4:"3", 5:"4", 6:"5", 7:"6", 8:"7", 9:"8", 10:"9", 11:"0"}

dev = InputDevice('/dev/input/event0')
print(dev)
while True:
    badge_read = ''
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY and event.value == 01:
            if event.code == 28:
                break
            elif event.code > 1 and event.code < 12:
                badge_read += decode_dict[event.code]
    now = datetime.datetime.now()
    encoder = DateTimeEncoder()
    dtjson = encoder.encode({"timestamp": now, "badge_id": badge_read})
    r = requests.post(
        'http://localhost:5000/api/scans',
        data=json.dumps(dtjson),
        headers={'Content-type': 'application/json'}
        )
    print badge_read
    print dtjson

