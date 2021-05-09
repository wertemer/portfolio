from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine  #Cоединение с СУБД
#from sqlalchemy.orm import scoped_session,sessionmaker

#Our configuration file
from config import Configuration

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './templates')
app=Flask(__name__,template_folder=template_path)
app.config.from_object(Configuration)
db=SQLAlchemy

#Нужно для использования уже существующие БД:
Base = declarative_base()
#Запросы
engine = create_engine(Configuration.SQLALCHEMY_DATABASE_URL, convert_unicode=True, echo=False)
Base.metadata.reflect(engine)