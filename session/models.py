import sqlite3
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    key = db.Column(db.String(120), index=True, unique=True)

    def __init__(self, userid):
        self.user_id = userid
        self.key = hashlib.sha224(str(userid) + now.strftime(DATE_FORMAT)).hexdigest()

    def __repr__(self):
        return '<id: %d, userid: %d, key: %s>' % (self.id, self.user_id, self.key)


class Users_s1(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(60), index=True, unique=True, nullable=False)
    password = db.Column(db.String(60), index=True, nullable=False)

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return '<userid: %d, login: %s, password: %s>' % (self.user_id, self.login, self.password)


