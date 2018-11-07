import psycopg2
import jwt


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
		return {'message': 'categort {} added'.format(items)},201
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
			return {'error': 'category name {} already exists'.format(items)}, 406
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
			return {'id':item[0][0], 'name': item[0][1]},200
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode: e.pgerror}


def delete(categoryId):
	con =connect()
	sql = """
	DELETE FROM category WHERE id = {}
	""".format(categoryId)
	try:
		cur = con.cursor()
		cur.execute(sql)
		con.commit()
		return {'message': 'record deleted'}, 202
	except psycopg2.Error as e:
		con.rollback()
		if int(e.pgcode) == 23503:
			return {'error': 'cannot delete becouse category is in use'},406
		else:
			return {e.pgcode: e.pgerror},500

def update(categoryId,name):
	old_name = one_category(categoryId)[0]['name']
	con =connect()
	sql = """
	UPDATE category SET name = '{}' WHERE id = {}
	""".format(name,categoryId)
	try:
		cur =con.cursor()
		cur.execute(sql)
		con.commit()
		return {'message': 'category name {} updated to {}'.format(old_name,name)},201
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode: e.pgerror},500


