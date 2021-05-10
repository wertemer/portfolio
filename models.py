import re,datetime
from app import db,Base

class tUsers(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	login=db.Column(db.String(120),nullable=False)
	password=db.Column(db.String(12),nullable=False)

class tAbout(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	public=db.Column(db.DateTime,nullable=False)
	about=db.Column(db.Text)

class tPortfolio(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	photo=db.Column(db.String(255),nullable=False)
	desc=db.Column(db.String(255),nullable=True)

class tContacts(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	contact=db.Column(db.String(255),nullable=True)
	contact=db.relationship('tIcons',backref='tContacts',lazy='dynamic')

class tIcons(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	icon=db.Column(db.String(255),nullable=True)
	desc=db.Column(db.String(255),nullable=True)
	contact=db.relationship('tContacts',backref='tIcons',lazy='dynamic')

class tContactIcons(db.Model):
	f_contact=db.Column(db.Integer,db.ForeignKey('tContacts.id')) #.relationship('tContacts')
	f_icon=db.Column(db.Integer,db.ForeignKey('tIcons.id'))
