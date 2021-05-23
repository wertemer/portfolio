from app import app,engine,db
from flask import render_template, redirect, flash, url_for, session,request
from models import tUsers, tAbout, tPortfolio, tContacts, dIcons, tContactIcons
from forms import LoginForm, AboutForm
#for agregation sql
from sqlalchemy import func
#for hashing passwords
import hashlib, datetime
#exceptions
from sqlalchemy.orm.exc import NoResultFound
#Страница сайта
@app.route('/') #,methods=['GET','POST']
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
	frmlogin=LoginForm()
	if frmlogin.validate_on_submit():
		user=tUsers.query.filter_by(login=frmlogin.login.data).first()
		if user==None:
			flash('Не верный Логин!')
		else:
			pas=hashlib.md5(frmlogin.password.data.encode('utf-8')).hexdigest()
			if user.password==pas:
				session['username']=frmlogin.login.data
				session['priv']='administrator'
				return redirect(url_for('admin'))
			else:
				flash('Пароль не Верен!')

	return render_template('login.html',form=frmlogin)

#Выход из профиля
@app.route('/logout', methods=['POST'])
def logout():
	session.clear()
	return redirect(url_for('login'))

@app.route('/admin',methods=['GET','POST'])
def admin():
	editabout=AboutForm(formdata=request.form)
	if 'username' in session:
		if session['username']=='Admin':
			about=db.session.query(tAbout,func.max(tAbout.public)).scalar()
			max_id=db.session.query(tAbout,func.max(tAbout.id)).scalar()
			print(max_id)
			print(max_id.id)
			print(about.about)
			print(about.public)
			if request.method=="POST":
				if editabout.validate_on_submit:
					date=str(editabout.dtime.data)
					text=editabout.text.data
					if about!=None:
						#записи уже есть
						if editabout.dtime.data!=None:
							publish=tAbout.query.filter_by(public=date).one_or_none()
							if publish!=None:
								print(publish.about)
								publish.about=text
								db.session.add(publish)
								print(publish.about)
								db.session.commit()
							else:
								#новая запись
								info=tAbout(public=date,about=text)
								db.session.add(info)
								db.session.commit()
						else:
							flash('Неверный формат даты!')
							return redirect(url_for('admin'))
					else:
						#первая запись
						info=tAbout(public=date,about=text)
						db.session.add(info)
						db.session.commit()
					return redirect(url_for('admin'))
			return render_template(
				'admin.html',
				ses=session,
				info=about,
				frm_a=editabout
			)
		else: redirect(url_for('login'))
	else: redirect(url_for('login'))
