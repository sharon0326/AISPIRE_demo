from datetime import timedelta

from flask import Flask
from flask_session import Session
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config.Config')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)  # 30 days login
#app.config['PERMANENT_SESSION_LIFETIME'] = 0
login = LoginManager(app)
login.login_view = 'login'


db = SQLAlchemy(app)
migrate = Migrate(app, db)
Session(app)

from app import routes, models



