#!/usr/local/env python
from evdev import InputDevice, categorize, ecodes
from dateutil.tz import tzlocal
from requests.auth import HTTPBasicAuth
import datetime
import json
import random
import requests
import string
import sys

from pi_userinfo import *

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()

        return super(DateTimeEncoder, self).default(obj)

def get_token(username, password):
    r = requests.post(
        'http://'+HOSTNAME+'/api/tokens',
        auth=HTTPBasicAuth(username, password)
        )
    if r.status_code != 200:
        return None
    json_token = json.loads(r.content)
    if 'token' not in json_token:
        return None
    return str(json_token["token"])

def randomString(stringLength=6):
    """Generate a random string with the combination of lowercase and uppercase letters """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

def request_create_user(new_badge):
    new_user_id = NEW_USER_PREFIX + randomString()
    user_dict = { "username": new_user_id, "password": NEW_USER_PASSWORD,
            "badge_id": new_badge }
    r = requests.post(
        'http://'+HOSTNAME+'/api/users',
        data=json.dumps(user_dict),
        headers={'Content-type': 'application/json',
            'Authorization': 'Bearer ' + MY_TOKEN},
        )
    print r.text

def get_a_badge_reading():
    decode_dict = {2:"1", 3:"2", 4:"3", 5:"4", 6:"5", 7:"6", 8:"7", 9:"8", 10:"9", 11:"0"}
    dev = InputDevice('/dev/input/event0')
    badge_read = ''
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY and event.value == 01:
            if event.code == 28:
                break
            elif event.code > 1 and event.code < 12:
                badge_read += decode_dict[event.code]
    return badge_read

def request_register_scan(badge_reading):
    localtz = tzlocal()
    now = datetime.datetime.now(localtz)
    encoder = DateTimeEncoder()
    dtjson = encoder.encode({"timestamp": now, "badge_id": badge_reading})
    r = requests.post(
        'http://'+HOSTNAME+'/api/scans',
        data=json.dumps(dtjson),
        headers={'Content-type': 'application/json',
            'Authorization': 'Bearer ' + MY_TOKEN},
        )
    print r.text

def event_loop():
    while True:
        badge_read = get_a_badge_reading()
        if badge_read == PIONEER_BADGE:
            # read the new badge
            new_badge = get_a_badge_reading()
            request_create_user(new_badge)
            badge_read = new_badge
        request_register_scan(badge_read)

if __name__ == "__main__":
    # get default password from file
    with open(NEW_USER_PASSWORD_FILE) as pfp:
        NEW_USER_PASSWORD = pfp.readline().strip()
    if len(NEW_USER_PASSWORD) < 6:
        print "the password is too short, needs to be > 6 chars"
        exit(1)

    # get pioneer badge
    with open(PIONEER_BADGE_FILE) as pfp:
        PIONEER_BADGE = pfp.readline().strip()
    if len(PIONEER_BADGE) < 10:
        print "doesn't appear to be a valid badge id"
        exit(1)

    # get my username
    with open(PI_USERNAME_FILE) as pfp:
        PI_USERNAME = pfp.readline().strip()
    if len(NEW_USER_PASSWORD) < 2:
        print "the username is too short, needs to be > 6 chars"
        exit(1)

    # get my password
    with open(PI_USER_PASSWORD_FILE) as pfp:
        PI_USER_PASSWORD = pfp.readline().strip()
    if len(NEW_USER_PASSWORD) < 6:
        print "the password is too short, needs to be > 6 chars"
        exit(1)

    MY_TOKEN = get_token(PI_USERNAME, PI_USER_PASSWORD)
    if MY_TOKEN is None:
        print "problem getting token, aborting"
        exit(1)

    event_loop()
