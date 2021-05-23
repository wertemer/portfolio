import re,datetime
from app import db, Base

class tUsers(db.Model):
	__tablename__='tUsers'
	id=db.Column(db.Integer,primary_key=True)
	login=db.Column(db.String(120),nullable=False)
	password=db.Column(db.String(255),nullable=False)

class tAbout(db.Model):
	__tablename__='tAbout'
	id=db.Column(db.Integer,primary_key=True)
	public=db.Column(db.DateTime,nullable=False)
	about=db.Column(db.Text)

class tPortfolio(db.Model):
	__tablename__='tPortfolio'
	id=db.Column(db.Integer,primary_key=True)
	photo=db.Column(db.String(255),nullable=False)
	desc=db.Column(db.String(255),nullable=True)

class tContacts(db.Model):
	__tablename__='tContacts'
	id=db.Column(db.Integer,primary_key=True)
	contact=db.Column(db.String(255),nullable=True)
	cico=db.relationship('tContactIcons',backref='tContacts',lazy='dynamic')

class dIcons(db.Model):
	__tablename__='dIcons'
	id=db.Column(db.Integer,primary_key=True)
	icon=db.Column(db.String(255),nullable=True)
	desc=db.Column(db.String(255),nullable=True)
	cico=db.relationship('tContactIcons',backref='dIcons',lazy='dynamic')

class tContactIcons(db.Model):
	__tablename__='tContactIcons'
	id=db.Column(db.Integer,primary_key=True)
	f_contact=db.Column(db.Integer,db.ForeignKey('tContacts.id'))
	f_icon=db.Column(db.Integer,db.ForeignKey('dIcons.id'))
