from sqlalchemy import text
from app import app, db
from app.models import User
from pi_userinfo import CONFIG_FILE

import configparser

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

if 'database' not in config.sections():
    print "Unable to read database configuration."
    exit(1)

DB_USER = config['database']['user']
DB_PASS = config['database']['pass']

b = text("DELETE FROM user")
result = db.engine.execute(b)

b = text("DELETE FROM scan")
result = db.engine.execute(b)

# check the username
if len(DB_USER) < 2:
    print "the username is too short, needs to be > 2 chars"
    exit(1)

# check the  password
if len(DB_PASS) < 6:
    print "the password is too short, needs to be > 6 chars"
    exit(1)


u = User(username=DB_USER, badge_id='0123456789', is_admin=True)
u.set_password(DB_PASS)

db.session.add(u)
db.session.commit()
