from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin(app)
login = LoginManager(app)
login.login_view = 'login'
from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

from app import routes, models
admin.add_view(models.AdminView(models.User, db.session))
admin.add_view(models.AdminView(models.Scan, db.session))
admin.add_link(models.LogoutMenuLink(name='Logout', category='', url="/logout"))

