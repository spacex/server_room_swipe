from sqlalchemy import text
from app import app, db
from app.models import User
from pi_userinfo import *



b = text("delete from user")
result = db.engine.execute(b)

b = text("delete from scan")
result = db.engine.execute(b)

# get my username
with open(PI_USERNAME_FILE) as pfp:
    PI_USERNAME = pfp.readline().strip()
if len(PI_USERNAME) < 2:
    print "the username is too short, needs to be > 6 chars"
    exit(1)

# get my password
with open(PI_USER_PASSWORD_FILE) as pfp:
    PI_USER_PASSWORD = pfp.readline().strip()
if len(PI_USER_PASSWORD) < 6:
    print "the password is too short, needs to be > 6 chars"
    exit(1)


u = User(username=PI_USERNAME, badge_id='0123456789', is_admin=True)
u.set_password(PI_USER_PASSWORD)

db.session.add(u)
db.session.commit()
