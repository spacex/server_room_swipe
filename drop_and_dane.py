from sqlalchemy import text
from app import app, db
from app.models import User, Badge

b = text("delete from user")
result = db.engine.execute(b)

b = text("delete from scan")
result = db.engine.execute(b)

b = text("delete from badge")
result = db.engine.execute(b)

u = User(username='dwilliams', email='dane.williams@raytheon.com', is_admin=True)
u.set_password("dane1234")
b = Badge(badge_id='12345678', username='dwilliams')

db.session.add(u)
db.session.add(b)
db.session.commit()
