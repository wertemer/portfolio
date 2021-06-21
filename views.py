from app import app,engine,db
from flask import render_template, redirect, flash, url_for, session,request
from models import tUsers, tAbout, tPortfolio, tContacts, dIcons, tContactIcons
from forms import LoginForm, AboutForm, AddContact, EditContact, UplFileP, AddIcon, OrderMail
#for agregation sql
from sqlalchemy import func
#for hashing passwords
import os, hashlib, datetime, json
#exceptions
from sqlalchemy.orm.exc import NoResultFound

from werkzeug.utils import secure_filename

#Удаление общей информации
@app.route('/deleteAbout',methods=['POST'])
def deleteAbout():
	about_id=request.form['id']
	about=tAbout.query.filter_by(id=about_id).one_or_none()
	if about!=None :
		db.session.delete(about)
		db.session.commit()
		msg='Общая информация по данной дате удалена!';
	else :
		msg='Нет общей информации по данной дате!!';
	jmsg={'msg':msg}
	json_string=json.dumps(jmsg)
	return json_string
#Удаление изображения из портфолио
@app.route('/delimg',methods=['POST'])
def delimg():
	photo_id=request.form['id']
	photo=tPortfolio.query.filter_by(id=photo_id).one()
	filename=photo.photo
	db.session.delete(photo)
	db.session.commit()
	#Удаляем файл с диска
	os.remove(filename)
	return redirect(url_for('admin'))
#Удаление иконки контакта
@app.route('/delicon', methods=['POST'])
def delicon():
	icon_id=request.form['id']
	icon=dIcons.query.filter_by(id=icon_id).one()
	filename=icon.icon
	db.session.delete(icon)
	db.session.commit()
	#Удаляем файл с диска
	os.remove(filename)
	return redirect(url_for('admin'))

#Получаем данные контакт через json
@app.route('/info_contact',methods=['POST'])
def info_contact():
	msg=''
	status=0
	ilist=[]
	jlist={}
	cid=request.form['cid']
	contact=tContacts.query.filter_by(id=cid).one_or_none()
	if contact==None:
		status=0
		msg='Контакт не найден!'
		jlist={ 'msg': msg, 'status':status }
	else :
		status=1
		msg='Контакт найден'
		cicon=tContactIcons.query.filter_by(f_contact=cid).all()
		#Создаем массив с данными о редактируемом контакте
		for ico in cicon:
			ilist.append(ico.f_icon)
		jlist={'msg':msg, 'status':status, 'id':contact.id, 'icons':ilist}
	#Создаем json с данными о редактируемом контакте и возвращаем его
	json_string = json.dumps(jlist)
	print(json_string)
	return json_string

#Удаляем контакт
@app.route("/delcontact",methods=["POST"])
def delcontact():
	id=int(request.form['id'])
	exist=tContacts.query.filter_by(id=id).one_or_none()
	if exist!=None:
		delconticons=tContactIcons.query.filter_by(f_contact=id).all()
		db.session.delete(delconticons)
		db.session.commit()
		delcont=tContacts.query.filter_by(id=id).one()
		db.session.delete(delcont)
		db.session.commit()
	else:
		print('none')
		flash('Контакт не найден!')
	return redirect(url_for('admin'))

#Страница сайта
@app.route('/') #,methods=['GET','POST']
def index():
	form=OrderMail()
	list_contacts=[]
	max_id=db.session.query(tAbout,func.max(tAbout.public)).one()
	about=tAbout.query.filter_by(public=max_id[1]).one_or_none()
	photos=tPortfolio.query.all()
	contacts=tContacts.query.all()
	for contact in contacts:
		icons=contact.getIcons()
		list_contacts.append(icons)
	if about!=None :
		info=about.about
	else:
		info=''
	if form.validate_on_submit():
		pass
	return render_template('index.html',info=info,portfolio=photos,contacts=list_contacts, form=form)

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

#delete row about
@app.route('/delabout', methods=['POST'])
def delAbout():
	pass

@app.route('/admin',methods=['GET','POST'])
def admin():
	editabout=AboutForm(formdata=request.form)
	portfolio=UplFileP(formdata=request.form)
	addcontact=AddContact(formdata=request.form)
	editcontact=EditContact(formdata=request.form)
	addicon=AddIcon(formdata=request.form)
	contacts=tContacts.query.all()
	pimg=tPortfolio.query.all()
	icons=dIcons.query.all()
	typecontact=[]
	acont=[]
	aicon=[]
	for ico in icons:
		typecontact.append((ico.id, ico.desc))
	for contact in contacts:
		for i in contact.cico:
			aicon.append(i.f_icon)
		acont.append({'id':contact.id, 'contact':contact.contact, 'icons':aicon})
		aicon=[]
	print(acont)
	addcontact.icons.choices=typecontact
	editcontact.eicons.choices=typecontact
	if 'username' in session:
		if session['username']=='Admin':
			max_id=db.session.query(tAbout,func.max(tAbout.public)).one()
			about=tAbout.query.filter_by(public=max_id[1]).one_or_none()
			if request.method=="POST":
				if editabout.validate_on_submit():
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
							editabout.dtime.data=''
							editabout.text.data=''
							return redirect(url_for('admin'))
						else:
							flash('Неверный формат даты!')
							return redirect(url_for('admin'))
					else:
						#первая запись
						info=tAbout(public=date,about=text)
						db.session.add(info)
						db.session.commit()
					return redirect(url_for('admin'))
				#Добавление портфолио
				if portfolio.validate_on_submit():
					#Получаем файлы из формы
					f=request.files['fname']
					#достаем путь к файлу
					filename = secure_filename(f.filename)
					#сохраняем файл
					f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					sf=app.config['UPLOAD_FOLDER']+filename
					#сохраняем путь к загруженному файлу в БД
					desc=portfolio.fdesc.data
					photo=tPortfolio(photo=sf,desc=desc)
					db.session.add(photo)
					db.session.commit()
					portfolio.fname.data=''
					portfolio.fdesc.data=''
					return redirect(url_for('admin'))
				#Добавление иконки
				if addicon.validate_on_submit():
					desc=addicon.idesc.data
					#Получаем файлы из формы
					f=request.files['icon']
					#достаем путь к файлу
					filename = secure_filename(f.filename)
					#сохраняем файл
					f.save(os.path.join(app.config['UPLOAD_ICON_CONTACT'], filename))
					sf=app.config['UPLOAD_ICON_CONTACT']+filename
					icon=dIcons(icon=sf, desc=desc)
					db.session.add(icon)
					db.session.commit()
					addicon.icon.data=''
					addicon.idesc.data=''
					return redirect(url_for('admin'))
				#Добавление контакта
				if addcontact.validate_on_submit():
					cont=addcontact.contact.data
					ico=addcontact.icons.data
					exist=tContacts.query.filter_by(contact=cont).one_or_none()
					if exist!=None:
						dcont=tContacts.query.filter_by(contact=cont).one()
						cont_id=dcont.id
						res=tContactIcons.query.filter_by(f_contact=cont_id).delete()
						for i in ico:
							contico=tContactIcons(f_contact=cont_id, f_icon=i)
							db.session.add(contico)
							db.session.commit()
							contico=''
					else:
						contact=tContacts(contact=cont)
						db.session.add(contact)
						db.session.commit()
						dcont=tContacts.query.filter_by(contact=cont).one()
						cont_id=dcont.id
						for i in ico:
							contico=tContactIcons(f_contact=cont_id, f_icon=i)
							db.session.add(contico)
							db.session.commit()
							contico=''
					addcontact.contact.data=''
					cont=''
					ico=[]
				#Редактируем контакт сохраняя данные в бд
				if editcontact.validate_on_submit():
					id=editcontact.eid.data
					contact=editcontact.econtact.data
					tcon=editcontact.eicons.data
					edcontact=tContacts.query.get(id)
					edcontact.contact=contact
					db.session.add(edcontact)
					db.session.commit()
					tContactIcons.query.filter_by(f_contact=id).delete()
					for ico in tcon:
						contico=tContactIcons(f_contact=id, f_icon=ico)
						db.session.add(contico)
						db.session.commit()
						contico=''
					editcontact.econtact.data=''
			return render_template(
				'admin.html',
				ses=session,
				info=about,
				frm_a=editabout,
				frm_p=portfolio,
				frm_c=addcontact,
				frm_b=editcontact,
				frm_add_ico=addicon,
				icontact=acont,
				pimg=pimg,
				icons=icons
			)
		else: redirect(url_for('login'))
	else: redirect(url_for('login'))
