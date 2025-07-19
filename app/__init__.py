from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect

import os
import dotenv
dotenv.load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-fallback-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thredly.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to view this page!'
    login_manager.login_message_category = 'info'

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    from . import auth, routes
    app.register_blueprint(routes.bp)
    app.register_blueprint(auth.bp, url_prefix='/auth')

    return app

