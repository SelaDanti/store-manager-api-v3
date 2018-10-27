import psycopg2

from flask import Flask

from .api.v2 import app_v2
from instance.config import app_config

def create_app(config):
	app = Flask(__name__)
	app.register_blueprint(app_v2)
	app.config.from_object(app_config[config])
	return app

def connect(self):
	db = app.config['DB']
	user = app.config['USER']
	host = app.config['HOST']
	password = app.config['PASSWORD']
	con = psycopg2.connect(db=db,user=user,host=host,password=password)
	return con

def create_database(self):
	sql_activation = """
	ID SERIAL PRIMARY_KEY,
	KEY INT NOT NULL
	"""
	sql_user = """
	ID SERIAL PRIMARY_KEY,
	FIRST_NAME VARCHAR(50) NOT NULL,
	LAST_NAME VARCHAR(50) NOT NULL,
	EMAIL VARCHAR(50) NOT NULL,
	PASSWORD VARCHAR(100) NOT NULL
	"""

	sql_category = """
	ID SERIAL PRIMARY_KEY,
	NAME VARCHAR(50) NOT NULL
	"""

	sql_product = """
	ID SERIAL PRIMARY_KEY,
	NAME VARCHAR(50) NOT NULL,
	QUANTITY INT NOT NULL,
	MIQ NOT NULL,
	CATEGORY_ID INT NOT
	"""


def destroy_database(self):
	pass