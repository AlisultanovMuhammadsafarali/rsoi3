import sqlite3
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Entries(db.Model):
    entry_id = db.Column(db.Integer, primary_key=True)
    user_fk = db.Column(db.Integer, index=True, nullable=False)
    title = db.Column(db.String(60), index=True, nullable=False)
    text = db.Column(db.String(140), index=True, nullable=False)

    def __init__(self, userid, usertitle, usertext):
    	self.entry_id 
        self.title = usertitle
        self.text = usertext

    def __repr__(self):
        return '<id: %d, title: %s, text %s>' % (self.id, self.title, self.text)
