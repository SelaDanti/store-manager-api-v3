import psycopg2
import jwt


from .... import connect

def products(id):
	con = connect()
	sql = """
	SELECT product_id, price FROM cart WHERE user_id = {}
	""".format(id)
	try:
		cur = con.cursor()
		cur.execute(sql)
		items = cur.fetchall()
		op = []
		for item in items:
			op.append({0:item[0],1:item[1]})
		return op
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode: e.pgerror}


def get_total(id):
	con = connect()
	sql = """
	SELECT price FROM cart WHERE user_id = {}
	""".format(id)
	try:
		cur = con.cursor()
		cur.execute(sql)
		items = cur.fetchall()
		total = 0
		for item in items:
			total += item[0]
		return total
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode: e.pgerror}

def insert_new_sale(total,user_id,dop,top):
	con = connect()
	sql = """
	INSERT INTO sale (total,user_id,dop,top) VALUES ({},{},'{}','{}')
	""".format(total,user_id,dop,top)
	try:
		cur = con.cursor()
		cur.execute(sql)
		con.commit()
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode: e.pgerror}

def clear_cart(id):
	con = connect()
	sql = """
	DELETE FROM cart WHERE user_id = {}
	""". format(id)
	try:
		cur = con.cursor()
		cur.execute(sql)
		con.commit()
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode: e.pgerror}

def check_cart(id):
	con = connect()
	sql = """
	SELECT * FROM cart WHERE user_id = {}
	""". format(id)
	try:
		cur = con.cursor()
		cur.execute(sql)
		item = cur.fetchall()
		if len(item) == 0:
			return False
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode: e.pgerror}

def get_all_sales():
	con =connect()
	sql = """
	SELECT * FROM sale
	"""
	try:
		cur = con.cursor()
		cur.execute(sql)
		items = cur.fetchall()
		ls = [{'message': 'List of sales'}]
		if len(items) == 0:
			return False
		else:
			for item in items:
				ls.append({'id':item[0],'total sale': item[1], 'dop': item[2],
					'dot': item[3]})
			return ls
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode: e.pgerror}


def get_by_id_attendant(id):
	con =connect()
	sql = """
	SELECT * FROM sale WHERE user_id = {}
	""".format(id)
	try:
		cur = con.cursor()
		cur.execute(sql)
		items = cur.fetchall()
		ls = []
		if len(items) == 0:
			return False
		else:
			for item in items:
				ls.append({'id':item[0],'products info': item[1], 'total sale': item[2],
					'user id': item[3]})
			return ls
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode: e.pgerror}

def get_by_id_admin(id):
	con =connect()
	sql = """
	SELECT * FROM sale WHERE id = {}
	""".format(id)
	try:
		cur = con.cursor()
		cur.execute(sql)
		items = cur.fetchall()
		ls = []
		if len(items) == 0:
			return False
		else:
			for item in items:
				ls.append({'id':item[0],'products info': item[1], 'total sale': item[2],
					'user id': item[3]})
			return ls
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode: e.pgerror}
