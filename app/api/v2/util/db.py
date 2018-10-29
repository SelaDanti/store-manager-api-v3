import psycopg2

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


# register
def add_user(items):
	con = connect()
	sql = """
	INSERT INTO users (FIRST_NAME, LAST_NAME, EMAIL, USER_TYPE, PASSWORD) VALUES
	('{}','{}','{}','{}','{}')
	""".format(items['first name'],items['last name'],items['email'],
		items['user type'],items['password'])
	try:
		cur = con.cursor()
		cur.execute(sql)
		con.commit()
		return True
	except psycopg2.Error as e:
		con.rollback()
		return{e.pgcode: e.pgerror}

