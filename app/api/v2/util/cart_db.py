import psycopg2
import jwt


from .... import connect
from .product_db import get_one_product

def insert_cart(items):
	con =connect()
	sql = """
	INSERT INTO cart(PRODUCT_ID,QUANTITY,PRICE) VALUES ({},{},{})
	""".format(items['product id'],items['quantity'],items['price'])
	try:
		cur  =con.cursor()
		cur.execute(sql)
		con.commit()
		return {'message': 'product added to cart'},201
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode:e.pgerror}


def decrement(id):
	con = connect()
	iq = get_one_product(id)[0]['quantity']
	nq = iq - id
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
	SELECT * FROM cart WHERE ID={}
	""".format(id)
	try:
		cur = con.cursor()
		cur.execute(sql)
		items = cur.fetchall()
		if len(items) > 0:
			return items
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode,e.pgerror}
