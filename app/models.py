from datetime import datetime, timedelta
from dateutil import parser
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
import base64
import os


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    email = db.Column(db.String(120), index=True, unique=True)
    badge_id = db.Column(db.String(10), unique=True)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return '{}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_user_from_badge(self, badge_id):
        return check_password_hash(self.password_hash, password)

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'badge_id']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def to_dict(self, include_email=False):
        data = {
		'id': self.id,
		'username': self.username,
		'badge_id': self.badge_id,
                }
        if include_email:
            data['email'] = self.email
        return data

    def get_token(self, expires_in=60):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), index=True, default=datetime.now)
    badge_id = db.Column(db.String(10), db.ForeignKey('user.badge_id'))
    device_name = db.Column(db.String(128))

    scanned_user = db.relationship("User", foreign_keys=[badge_id])

    def from_dict(self, data):
        for field in ['badge_id', 'timestamp', 'device_name']:
            if field in data:
                if field == 'timestamp':
                    real_datetime = parser.parse(data[field])
                    setattr(self, field, real_datetime)
                else:
                    setattr(self, field, data[field])

    def to_dict(self):
        return {
            'badge_id': self.badge_id,
            'timestamp': self.timestamp,
            'device_name': self.device_name,
        }

    def to_list(self):
        return [self.badge_id, self.timestamp, self.device_name]

class PioneerBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    badge_id = db.Column(db.String(10))

class AdminView(ModelView):
    @expose('/admin')
    def index(self):
        return self.render('admin')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class LogoutMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated  
