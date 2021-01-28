from flask_login import UserMixin
from . import db

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128))
    events = db.relationship('Event', backref='User', uselist=False)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    category = db.Column(db.String(50))    
    place = db.Column(db.String(50)) 
    address = db.Column(db.String(50)) 
    dateIni = db.Column(db.DateTime)
    dateFinal = db.Column(db.DateTime)
    isVirtual = db.Column(db.Boolean, default=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
