from app import app,engine
from flask import render_template, redirect

#Страница сайта
@app.route('/') #,methods=['GET','POST']
def index():
	return render_template('index.html')
