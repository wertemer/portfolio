import re,datetime
from app import db,Base
#Модели таблиц
#Уже существующая таблица!

class tUsers(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	login=db.Column(db.String(120),null=False)
	password=db.Column(db.String(12),null=False)

class tAbout(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	public=db.Column(db.DateTime,null=False)
	about=db.Column(db.Text)

class tPortfolio(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	photo=db.Column(db.String(255),null=False)
	desc=db.Column(db.String(255),null=True)

class tContacts(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	contact=db.Column(db.String(255),null=True)

class tIcons(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	icon=db.Column(db.String(255),null=True)
	desc=db.Column(db.String(255),null=True)

class tContactIcons(db.Model):
	f_contact=db.relationship('tContacts')
	f_icon=db.relationship('tIcons')
