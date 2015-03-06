import sqlite3
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(64), index = True)
    email = db.Column(db.String(120), index = True, unique = True)
    phone = db.Column(db.String(20), index = True, unique = True)

    def __init__(self, nickname, password, email, phone):
        self.nickname = nickname
        self.password = password
        self.email = email
        self.phone = phone

    def __repr__(self):
        return '<id: %d, nickname: %s, email: %s>' % (self.id, self.nickname, self.email)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(60))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_fk = db.Column(db.Integer)

    def __repr__(self):
        return '<Title: %s, Post %r>' % (self.text)


