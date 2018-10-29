import psycopg2
import os

from flask import Flask

from instance.config import app_config


env = os.environ.get('ENV')
def create_app():
	from .api.v2 import app_v2
	app = Flask(__name__)
	app.register_blueprint(app_v2)
	app.config.from_object(app_config[env])
	return app

def connect():
	app = create_app()
	db = app.config['DATABASE_NAME']
	user = app.config['USER']
	host = app.config['HOST']
	password = app.config['PASSWORD']
	con = psycopg2.connect(database=db,user=user,host=host,password=password)
	return con

def sqls():
	sql_activation = """
	CREATE TABLE IF NOT EXISTS activate(
	ID SERIAL PRIMARY KEY,
	KEY VARCHAR(10) NOT NULL,
	STATUS VARCHAR(40) NOT NULL)
	"""
	sql_user = """
	CREATE TABLE IF NOT EXISTS users(
	ID SERIAL PRIMARY KEY,
	FIRST_NAME VARCHAR(50) NOT NULL,
	LAST_NAME VARCHAR(50) NOT NULL,
	EMAIL VARCHAR(50) NOT NULL,
	USER_TYPE VARCHAR(50) NOT NULL,
	PASSWORD VARCHAR(100) NOT NULL)
	"""

	sql_category = """
	CREATE TABLE IF NOT EXISTS category(
	ID SERIAL PRIMARY KEY,
	NAME VARCHAR(50) NOT NULL)
	"""

	sql_product = """
	CREATE TABLE IF NOT EXISTS products(
	ID SERIAL PRIMARY KEY,
	NAME VARCHAR(50) NOT NULL,
	QUANTITY INT NOT NULL,
	MIQ INT NOT NULL,
	UOM VARCHAR(50) NOT NULL,
	USER_ID INT NOT NULL references users(ID),
	CATEGORY_ID INT NOT NULL references category(ID))
	"""
	return [sql_activation,sql_category,sql_user,sql_product]

def create_database():
	con = connect()
	try:
		for sql in sqls():
			cur = con.cursor()
			cur.execute(sql)
			con.commit()
	except psycopg2.Error as e:
		print(e.pgerror)

def set_key():
	con = connect()
	sql = """
	SELECT * FROM activate WHERE ID=1
	"""
	sql2 = """
	INSERT INTO activate (KEY,STATUS) VALUES ('12345','False')
	"""
	try:
		cur = con.cursor()
		cur.execute(sql)
		item = cur.fetchone()
		if item is None:
			cur.execute(sql2)
			con.commit()
	except psycopg2.Error as e:
		print(e.pgerror)



def destroy_tables():
	con = connect()
	sql_product = """
	DROP TABLE products
	"""
	sql_category = """
	DROP TABLE category
	"""
	sql_user = """
	DROP TABLE users
	"""
	sql_activation = """
	DROP TABLE activate
	"""
	sqls = [sql_product,sql_category,sql_user, sql_activation]

	try:
		for sql in sqls:
			cur = con.cursor()
			cur.execute(sql)
			con.commit()
	except psycopg2.Error as e:
		print(e.pgerror)
