import sqlite3
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), index=True, nullable=False)
    text = db.Column(db.String(140), index=True, nullable=False)

    def __init__(self, usertitle, usertext):
        self.title = usertitle
        self.text = usertext

    def __repr__(self):
        return '<id: %d, title: %s, text %s>' % (self.id, self.title, self.text)
