from app import db
from app import login

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

import sqlalchemy.dialects.postgresql


class Users(UserMixin, db.Model):
    """user accounts table for granting access"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Employee(db.Model):
    """all employee of organization"""
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), index=True)
    work_start = db.Column(db.Date, index=True)
    salary = db.Column(db.Numeric(5,2), index=True)
    position = db.Column(db.String(120), index=True)
    manager_id = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '''<{1}, id: {0}, pos: {2}>'''.format(
            self. id, self.full_name, self.position)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
