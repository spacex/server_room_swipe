from flask_wtf import FlaskForm
from datetime import datetime, timedelta
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields.html5 import DateField
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ExportForm(FlaskForm):
    start_date = DateField('Start Date', default=datetime.today, format='%Y-%m-%d')
    end_date = DateField('End Date', default=datetime.today, format='%Y-%m-%d')
    submit = SubmitField('Export')

