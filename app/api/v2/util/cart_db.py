import psycopg2
import jwt


from .... import connect
from .product_db import get_one_product
from .auth import get_user

def insert_cart(items):
	product_name = get_one_product(items['product id'])[0]['product name']
	con =connect()
	sql = """
	INSERT INTO cart(PRODUCT_ID,QUANTITY,PRICE,USER_ID) VALUES ({},{},{},{})
	""".format(items['product id'],items['quantity'],items['price'],get_user()['id'])
	try:
		cur  =con.cursor()
		cur.execute(sql)
		con.commit()
		return {'message': 'product {} added to cart'.format(product_name)},201
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode:e.pgerror}


def decrement(id,quantity):
	con = connect()
	iq = get_one_product(id)[0]['quantity']
	nq = iq - quantity
	sql = """
	UPDATE products SET quantity = {} WHERE id={}
	""".format(nq,id)
	try:
		cur = con.cursor()
		cur.execute(sql)
		con.commit()
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode,e.pgerror}

def already_exist(id):
	con =connect()
	sql = """
	SELECT * FROM cart WHERE PRODUCT_ID={}
	""".format(id)
	try:
		cur = con.cursor()
		cur.execute(sql)
		items = cur.fetchall()
		if len(items) > 0:
			return False
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode,e.pgerror}


def get_cart_quantity(id):
	con = connect()
	sql = """
	SELECT quantity FROM cart WHERE product_id = {}
	""".format(id)
	try:
		cur = con.cursor()
		cur.execute(sql)
		items = cur.fetchone()
		return items[0]
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode,e.pgerror}


def increment(id,quantity):
	product_name = get_one_product(id)[0]['product name']
	con = connect()
	iq = get_cart_quantity(id)
	nq = iq + quantity
	sql = """
	UPDATE cart SET quantity = {} WHERE product_id={}
	""".format(nq,id)
	try:
		cur = con.cursor()
		cur.execute(sql)
		con.commit()
		return {'message': 'quantity of {} incremented to {}'.format(product_name,nq)},201
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode,e.pgerror}


def get_all_cart():
	con = connect()
	sql = """
	SELECT * FROM cart 
	"""
	try:
		cur =con.cursor()
		cur.execute(sql)
		items = cur.fetchall()
		op = [{'message': 'list of my carts'}]
		for item in items:
			x = {'id': item[0], 'product id': item[1], 'quantity': item[3],'price': item[4]}
			op.append(x)
		if len(op) == 1:
			return {'error': 'carts is empty'},404
		else:
			return op
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode,e.pgerror}


def get_cart_item(id):
	con = connect()
	sql = """
	SELECT * FROM cart WHERE product_id={}
	""".format(id)
	try:
		cur =con.cursor()
		cur.execute(sql)
		items = cur.fetchall()
		if len(items) == 0:
			return {'error': 'cart id not found'},404
		else:
			op = []
			for item in items:
				x = {'id': item[0], 'product id': item[1],'user id': item[2],
				'quantity': item[3],'price': item[4]}
				op.append(x)
			return op
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode,e.pgerror}


def revert_back(q,i):
	con = connect()
	sql = """
	UPDATE products SET quantity = {} WHERE id = {}
	""".format(q,i)
	try:
		cur = con.cursor()
		cur.execute(sql)
		con.commit()
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode,e.pgerror}


def delete_cart(producId):
	con = connect()
	sql = """
	DELETE FROM cart WHERE product_id = {}
	""".format(producId)
	try:
		cur = con.cursor()
		cur.execute(sql)
		con.commit()
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode,e.pgerror}

def convert_to_id(name):
	con = connect()
	sql = """
	SELECT id FROM products WHERE name = '{}'
	""".format(name)
	try:
		cur = con.cursor()
		cur.execute(sql)
		items = cur.fetchone()
		if items is None:
			return -1
		else:
			return items[0]
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode,e.pgerror}