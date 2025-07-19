from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import Length, DataRequired, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

import json

import os
import dotenv
dotenv.load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-fallback-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thredly.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = '❗ Please log in to view this page!'
login_manager.login_message_category = 'info'
csrf = CSRFProtect(app)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(254), nullable=False)

    def __repr__(self):
        return f'<User username={self.username}, id={self.id}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class UserCreationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Username is required.',), Length(min=3, max=64, message='Username must be between 3 and 64 characters.')], description='Enter a unique username (3-64 characters).')
    password = PasswordField('Password', validators=[DataRequired(message='Password is required.'), Length(min=6, message='Password must be at least 6 characters long.')], description='Create a strong password (min. 6 characters).')
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(message='Please confirm your password.'), EqualTo('password', message='Passwords must match.')], description='Re-enter your password.')
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Username is required.',), Length(min=3, max=64, message='Username must be between 3 and 64 characters.')],
        description='Your unique login name. It is usually assigned or created during registration.')
    password = PasswordField('Password', validators=[DataRequired(message='Password is required.'), Length(min=6, message='Password must be at least 6 characters long.')],
        description='Use a strong password with at least 6 characters, including letters and numbers.')
    submit = SubmitField('Login')


# ============== ROUTES ==============


@app.route('/')
@app.route('/home')
def home():
    with open('data/threads.json', 'r', encoding='utf-8') as f: threads = json.load(f)
    return render_template('home.html', threads=threads)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UserCreationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('✅ Your account has been successfully created.  Please log in now!', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('✅ You have successfully logged in!', category='success')
            return redirect(next_page or url_for('home'))
        else:
            flash('⚠️ Invalid username or password', 'warning')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('‼️ You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print(f' * {app.config['SQLALCHEMY_DATABASE_URI']} is active!')
    app.run(debug=True, host='0.0.0.0')