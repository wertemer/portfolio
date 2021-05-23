from flask import Flask
from flask_wtf import FlaskForm,RecaptchaField#,widgets
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,DateTimeField,FileField,SelectMultipleField,IntegerField
from wtforms.validators import Required,DataRequired,Email,Length

#from werkzeug.utils import secure_filename

#from flask_uploads import UploadSet, IMAGES
#Для чекбоксов
from wtforms import widgets

#images = UploadSet('images', IMAGES)

#Форма отправки заказа
class OrderMail(FlaskForm):
	phone=StringField('Введите Ваш номер телефона*:',validators=[DataRequired()],render_kw={'Placeholder':'+X(XXX)XXX XX XX'})
	email=StringField('Введите Ваш E-mail*:',validators=[Email()],render_kw={'Placeholder':'sample@sample.com'})
	desc=TextAreaField('Краткое описание заказа*',validators=[DataRequired()])
	submit=SubmitField('Заказать')

#Форма отправки смс
class SmsMail(FlaskForm):
	phone=StringField('Введите Ваш номер телефона*:',validators=[DataRequired()],render_kw={'Placeholder':'+X(XXX)XXX XX XX'})
	submit=SubmitField('Отправить')

#Форма входа
class LoginForm(FlaskForm):
	login=StringField('Логин:',validators=[DataRequired()],render_kw={'Placeholder':'Введите Ваш Логин'})
	password=PasswordField('Пароль:',validators=[DataRequired()],render_kw={'Placeholder':'Введите Ваш Пароль'})
	#recaptcha = RecaptchaField()
	submit=SubmitField('Войти')

#Форма для редактирования общей информации
class AboutForm(FlaskForm):
	dtime=date=DateTimeField('Дата текста:', format='%Y-%m-%d %H:%M:%S', validators=[])#DataRequired(),Required()
	text=TextAreaField('Обо мне',validators=[DataRequired()])
	submit=SubmitField('Сохранить')

#Форма для загрузки файла портфолио
#class UplFileP(FlaskForm):
#	fname=FileField('Выберите файл:',validators=[FileAllowed(images, 'Images only!')])
#	fdesc=StringField('Описание:',validators=[DataRequired()],render_kw={'Placeholder':'Введите описание файла портфолио'})
#	submit=SubmitField('Загрузить')

#Checkboxes
class MultiCheckboxField(SelectMultipleField):
	widget=widgets.ListWidget(prefix_label=False)
	option_widget=widgets.CheckboxInput()

#Форма для добавления контакта
class AddContact(FlaskForm):
	contact=StringField('Введите новый контакт:',validators=[DataRequired(),Required('Введите контакт')])
	choices=[]
	icons=MultiCheckboxField('Вид контакта:',choices=choices,coerce=int)
	submit=SubmitField('Добавить')

#Форма редактирования контакта
class EditContact(FlaskForm):
	econtact=StringField('Kонтакт:')
	eid=IntegerField('id',validators=[DataRequired()])
	echoices=[]
	eicons=MultiCheckboxField('Вид контакта:',choices=echoices,coerce=int)
	esubmit=SubmitField('Сохранить')
