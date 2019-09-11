from sqlalchemy import text
from app import app, db
from app.models import User

b = text("delete from user")
result = db.engine.execute(b)

b = text("delete from scan")
result = db.engine.execute(b)

u = User(username='dwilliams', badge_id='0123456789', email='dane.williams@raytheon.com', is_admin=True)
u.set_password("dane1234")

db.session.add(u)
db.session.commit()
