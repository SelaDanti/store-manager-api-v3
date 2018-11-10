import psycopg2
import jwt

from werkzeug.security import check_password_hash

from .... import connect

# activation query
def fetch_activation():
	con = connect()
	sql = """
	SELECT key, status FROM activate WHERE id = 1
	"""
	try:
		cur = con.cursor()
		cur.execute(sql)
		item = cur.fetchall()
		return item[0]
	except psycopg2.Error as e:
		con.rollback()
		return{e.pgcode: e.pgerror}

def activate():
	con = connect()
	sql = """
	UPDATE activate SET status = 'True' WHERE id =1
	"""
	try:
		cur = con.cursor()
		cur.execute(sql)
		con.commit()
		return True
	except psycopg2.Error as e:
		con.rollback()
		return{e.pgcode: e.pgerror}


# attendants queries
def add_user(items):
	con = connect()
	sql = """
	INSERT INTO users (FIRST_NAME, LAST_NAME, EMAIL, USER_TYPE, PASSWORD) VALUES
	('{}','{}','{}','{}','{}')
	""".format(items['first name'],items['last name'],items['email'].lower(),
		items['user type'],items['password'])
	try:
		cur = con.cursor()
		cur.execute(sql)
		con.commit()
		return True
	except psycopg2.Error as e:
		con.rollback()
		return{e.pgcode: e.pgerror}

def email_exist(email):
	con = connect()
	sql = """
	SELECT email FROM users WHERE email= '{}'
	""".format(email.lower())
	try:
		cur = con.cursor()
		cur.execute(sql)
		item = cur.fetchone()
		return item
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode: e.pgerror}

def get_accounts():
	con =connect()
	sql = """
	SELECT * FROM users WHERE user_type != 'super admin'
	"""
	try:
		cur = con.cursor()
		cur.execute(sql)
		items = cur.fetchall()
		if len(items) == 0:
			return {'message': 'no record found'},404
		else:
			ls = []
			for item in items:
				x = {
				'id': item[0],
				'first name': item[1],
				'last name': item[2],
				'email': item[3],
				'user type': item[4]
				}
				ls.append(x)
			return ls
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode :e.pgerror}

def get_account(accountId):
	con =connect()
	sql = """
	SELECT * from users WHERE id = {}
	""".format(accountId)
	try:
		cur = con.cursor()
		cur.execute(sql)
		item = cur.fetchall()
		if len(item) == 0:
			return {'message': 'record not found'},404
		else:
			op = {
			'id': item[0][0],
			'first name': item[0][1],
			'last name': item[0][2],
			'email': item[0][3],
			'user type': item[0][4]
			}
			return op,200
	except psycopg2.Error as e:
		con.rollback()
		return {'error': 'invalid id'},406

def update_user_type(attendantId,user_type):
	con = connect()
	sql = """
	UPDATE users SET user_type= '{}' WHERE id = {}
	""".format(user_type,attendantId)
	try:
		cur = con.cursor()
		cur.execute(sql)
		con.commit()
		return True
	except psycopg2.Error as e:
		return {e.pgcode,e.pgerror}



# check password and email
def password_checker(email,password):
	con =connect()
	sql = """
	SELECT id,password, user_type FROM users WHERE email = '{}'
	""".format(email)
	try:
		cur = con.cursor()
		cur.execute(sql)
		items = cur.fetchall()
		if len(items) == 0:
			return {'error': 'invalid email or password'}, 406
		else:
			if check_password_hash(items[0][1],password) is True:
				token = jwt.encode({'id': items[0][0],'type': items[0][2]},'12345', algorithm='HS256')
				token = token.decode('UTF-8')
				return {'message': {'token':token}}
			else:
				return {'error': 'invalid username or password'},406
	except psycopg2.Error as e:
		con.rollback()
		return {e.pgcode: e.pgerror}

