from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from .forms import UserCreationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    form = UserCreationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been successfully created.  Please log in now!', category='success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('You have successfully logged in!', category='success')
            return redirect(next_page or url_for('routes.home'))
        else:
            flash('Invalid username or password', 'warning')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))