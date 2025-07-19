from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from .models import User

class UserCreationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Username is required.',), Length(min=3, max=64, message='Username must be between 3 and 64 characters.')], description='Enter a unique username (3-64 characters).')
    password = PasswordField('Password', validators=[DataRequired(message='Password is required.'), Length(min=6, message='Password must be at least 6 characters long.')], description='Create a strong password (min. 6 characters).')
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(message='Please confirm your password.'), EqualTo('password', message='Passwords must match.')], description='Re-enter your password.')
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Username is required.',), Length(min=3, max=64, message='Username must be between 3 and 64 characters.')],
        description='Your unique login name. It is usually assigned or created during registration.')
    password = PasswordField('Password', validators=[DataRequired(message='Password is required.'), Length(min=6, message='Password must be at least 6 characters long.')],
        description='Use a strong password with at least 6 characters, including letters and numbers.')
    submit = SubmitField('Login')