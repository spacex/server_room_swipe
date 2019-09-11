from datetime import datetime, timedelta
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import base64
import os


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    email = db.Column(db.String(120), index=True, unique=True)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def to_dict(self, include_email=False):
        data = {
		'id': self.id,
		'username': self.username,
                }
        if include_email:
            data['email'] = self.email
        return data

    def get_token(self, expires_in=3600):
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
class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Integer, db.ForeignKey('user.id'))
    badge_id = db.Column(db.String(10), unique=True)
    def from_dict(self, data):
        for field in ['badge_id', 'username']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
		'badge_id': self.badge_id,
		'username': self.username,
                }
        return data



class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    badge_id = db.Column(db.String(10), db.ForeignKey('badge.badge_id'))

    def from_dict(self, data):
        for field in ['badge_id', 'timestamp']:
            if field in data:
                if field == 'timestamp':
                    real_datetime = datetime.strptime(data[field], '%Y-%m-%dT%H:%M:%S.%f')
                    setattr(self, field, real_datetime)
                else:
                    setattr(self, field, data[field])

    def to_dict(self):
        data = {
		'badge_id': self.badge_id,
		'timestamp': self.timestamp,
                }
        return data





