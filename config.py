import os

class Configuration():
	APPLICATION_DIR=os.path.dirname(os.path.realpath(__file__))
	TEMPLATES_AUTO_RELOADED=True
	SECRET_KEY='adfhsajgfiywqryq03ur2093uq09fpoa]gojw9ur98q23y4r7tyfgshvbfakhaufhiuagrfiaeh5iuh'
	DEBUG=True
	SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:gothic1321@localhost/mysite"

	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_POOL_SIZE = 200
	SQLALCHEMY_MAX_OVERFLOW = 5
	SQLALCHEMY_POOL_RECYCLE = 5

	MAIL_SERVER='smtp.gmail.com'
	MAIL_PORT=587
	MAIL_USE_TLS=True
	MAIL_USE_SSL=False

	MAIL_USERNAME = 'ssender097@gmail.com'
	MAIL_PASSWORD = 'yfnecz_1321'

	UPLOAD_FOLDER='./static/images/portfolio/'
	UPLOAD_ICON_CONTACT='./static/images/icons/contacts/'
