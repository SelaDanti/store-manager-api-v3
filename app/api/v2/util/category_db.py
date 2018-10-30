import psycopg2
import jwt

from werkzeug.security import check_password_hash

from .... import connect


def insert_category(items):
	con = connect()
	sql = """
	INSERT INTO category (NAME) VALUES ('{}')
	""".format(items)
	try:
		cur = con.cursor()
		cur.execute(sql)
		con.commit()
		return {'message': 'categort added'},201
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode: e.pgerror}


def category_name_exist(items):
	con =connect()
	sql = """
	SELECT * FROM category WHERE name = '{}'
	""".format(items)
	try:
		cur = con.cursor()
		cur.execute(sql)
		item = cur.fetchall()
		if len(item) == 0:
			return True
		else:
			return {'error': 'category name already exists'}, 406
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode: e.pgerror}


def all_categories():
	con =connect()
	sql = """
	SELECT * from category
	"""
	try:
		cur = con.cursor()
		cur.execute(sql)
		items = cur.fetchall()
		if len(items) == 0:
			return {'error': 'no record found'}, 404
		else:
			ls = []
			for item in items:
				ls.append({'id':item[0], 'name': item[1]})
			return ls,200
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode: e.pgerror}


def one_category(categoryId):
	con = connect()
	sql = """
	SELECT * FROM category WHERE id = {}
	""".format(categoryId)
	try:
		cur = con.cursor()
		cur.execute(sql)
		item = cur.fetchall()
		if len(item) == 0:
			return {'error': 'no record found'}, 404
		else:
			return {'id':item[0][0], 'name': item[0][1]}
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode: e.pgerror}


