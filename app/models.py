from app import db
import sqlalchemy.dialects.postgresql

class User(db.Model):
    """user accounts table for granting access"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Employee(db.Model):
    """all employee of organization"""
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), index=True)
    work_start = db.Column(db.DateTime, index=True)
    salary = db.Column(db.Numeric(5,2), index=True)
    position = db.Column(db.String(120), index=True)
    manager_id = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '''<{1}, id: {0}, pos: {2}>'''.format(
            self. id, self.full_name, self.position)
