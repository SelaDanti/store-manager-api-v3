import unittest
import json

from app import create_app, create_database,set_key, destroy_tables
from .common import post, create_super_admin, super_admin_token,get


class TestActivate(unittest.TestCase):
	def setUp(self):
		create_database()
		set_key()
		self.test = create_app().test_client()
		self.content_type = 'application/json'
		self.data = {'first name': 'john', 'last name': 'doe',
		'email': 'alex@gmail.com', 'password': 'password',
		'user type': 'attendant'}
		self.url = 'api/v2/attendants'
		create_super_admin(self.test,self.content_type)
		self.headers = {'X-API-KEY': '{}'.format(super_admin_token(self.test,self.content_type))}

	def tearDown(self):
		self.test = None
		self.content_type = None
		self.url = None
		self.data = None
		destroy_tables()

	def test_not_logged_in(self):
		res = post(self.test,self.url,self.data,self.content_type)
		data =json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'token is missing'})
		self.assertEqual(res.status_code,401)

	def test_invalid_token(self):
		self.headers = {'X-API-KEY': 'no token'}
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'token is invalid'})
		self.assertEqual(res.status_code,401)

	def test_empty_data(self):
		self.data['first name'] = ''
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data =json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'empty data set - first name'})
		self.assertEqual(res.status_code,406)

	def test_whitespace_data(self):
		self.data['first name'] = '  '
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data =json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'whitespace data set - first name'})
		self.assertEqual(res.status_code,406)

	def test_not_mail(self):
		self.data['email'] = 'nonmail.com'
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid email'})
		self.assertEqual(res.status_code,406)

	def test_not_role(self):
		self.data['user type'] = 'notrole'
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid role'})
		self.assertEqual(res.status_code,406)

	def test_extra_payload(self):
		self.data['extra'] = 'extra payload'
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid payload'})

	def test_min_payload(self):
		del self.data['email']
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid payload'})

	def test_email_already_exist(self):
		post(self.test,self.url,self.data,self.content_type,self.headers)
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'email already exist'})
		self.assertEqual(res.status_code,406)

	def test_valid_data(self):
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'message': 'new attendant added'})
		self.assertEqual(res.status_code,201)

	def test_get_no_attendants(self):
		res = get(self.test,self.url,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'message': 'no record found'})
		self.assertEqual(res.status_code,404)

	def test_get_attendants(self):
		post(self.test,self.url,self.data,self.content_type,self.headers)
		res = get(self.test,self.url,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(res.status_code,200)

	
if __name__ == '__main__':
	unittest.main()