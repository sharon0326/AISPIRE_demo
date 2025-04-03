from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy import Enum
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(Enum('individual', 'business', name='user_types'), nullable=False)
    company_name = db.Column(db.String(120), nullable=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

    def __repr__(self):
        return f'<User {self.username} ({self.user_type})>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class EssayHistory(db.Model):
    __tablename__ = 'essay_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    generated_time = db.Column(db.DateTime, default=datetime.utcnow)
    topic = db.Column(db.String(500), nullable=False)
    notes = db.Column(db.String(500), nullable=False)
    word_limit = db.Column(db.String(20), nullable=False)
    outline_type = db.Column(db.String(50), nullable=False)
    selected_outline = db.Column(db.Text, nullable=False)
    generated_essay = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Essay {self.id} - User {self.user_id}>'

