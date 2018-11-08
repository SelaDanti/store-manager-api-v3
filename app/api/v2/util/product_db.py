import psycopg2
import jwt


from .... import connect

def insert_product(items):
	con = connect()
	sql = """
	INSERT INTO products (NAME,QUANTITY,MIQ,CATEGORY_ID,UOM,PRICE) VALUES ('{}',{},{},{},'{}',{})
	""".format(items['product name'].lower(),items['quantity'],items['miq'],items['category id'],items['uom'],items['price'])
	try:
		cur = con.cursor()
		cur.execute(sql)
		con.commit()
		return {'message': 'product {} added'.format(items['product name'])},201
	except psycopg2.Error as e:
		con.rollback()
		if int(e.pgcode) == 23505:
			return {'error': 'product already exists'},406
		


def update_product(items,id):
	con =connect()
	sql = """
	UPDATE products SET name= '{}', quantity = {},miq = {}, category_id = {},uom = '{}' WHERE ID={}
	""".format(items['product name'].lower(),items['quantity'],items['miq'],items['category id'],items['uom'],id)
	try:
		cur = con.cursor()
		cur.execute(sql)
		con.commit()
		return {'message': 'product {} updated'.format(items['product name'])},201
	except psycopg2.Error as e:
		con.rollback()
		if int(e.pgcode) == 23505:
			return {'error': 'product {} already exists'.format(items['product name'])}, 406
		return {e.pgcode:e.pgerror}

def get_one_product(id):
	con =connect()
	sql = """
	SELECT * FROM products WHERE ID = {}
	""".format(id)
	try:
		cur = con.cursor()
		cur.execute(sql)
		items = cur.fetchall()
		if len(items) == 0:
			return {'error': 'product not found'},404
		else:
			op = {'id':items[0][0],'product name': items[0][1],'quantity': items[0][2],
			'uom': items[0][3],'category id': items[0][4],'price': items[0][5]}
			return op,200
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode:e.pgerror}

def get_all_product():
	con =connect()
	sql = """
	SELECT * FROM products
	""".format(id)
	try:
		cur = con.cursor()
		cur.execute(sql)
		items = cur.fetchall()
		if len(items) == 0:
			return {'error': 'product not found'},404
		else:
			op = []
			for item in items:
				op.append({'id':item[0],'product name': item[1],'quantity': item[2],
			'uom': item[3],'category id': item[4]})
			return op,200
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode:e.pgerror}

def delete_product(id):
	con =connect()
	product_name = get_one_product(id)[0]['product name']
	sql = """
	DELETE FROM products WHERE ID={}
	""".format(id)
	try:
		cur =con.cursor()
		cur.execute(sql)
		con.commit()
		return {'message': 'product {} deleted'.format(product_name)}, 202
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode:e.pgerror}