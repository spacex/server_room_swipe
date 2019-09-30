from flask_wtf import FlaskForm
from datetime import datetime, timedelta
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields.html5 import DateField
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    is_admin = BooleanField('Administrator?')
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class ExportForm(FlaskForm):
    export_type = SelectField('Export Type', choices=[('xlsx', 'XLSX'), ('csv', 'CSV')],
        default='xlsx')
    start_date = DateField('Start Date', default=datetime.today, format='%Y-%m-%d')
    end_date = DateField('End Date', default=datetime.today, format='%Y-%m-%d')
    submit = SubmitField('Export')

