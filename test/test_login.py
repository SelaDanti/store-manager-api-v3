import unittest
import json

from app import create_app, create_database,set_key, destroy_tables
from .common import post, create_super_admin


class TestActivate(unittest.TestCase):
	def setUp(self):
		create_database()
		set_key()
		self.test = create_app().test_client()
		self.content_type = 'application/json'
		self.data = {'email': 'john@gmail.com', 'password': 'password'}
		self.url = 'api/v2/auth/login'
		create_super_admin(self.test,self.content_type)

	def tearDown(self):
		self.test = None
		self.content_type = None
		self.url = None
		self.data = None
		destroy_tables()

	def test_empty_data(self):
		self.data['password'] = ''
		res = post(self.test,self.url,self.data,self.content_type)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'empty data set - password'})
		self.assertEqual(res.status_code,406)

	def test_white_space(self):
		self.data['password'] = '  '
		res = post(self.test,self.url,self.data,self.content_type)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'whitespace data set - password'})
		self.assertEqual(res.status_code,406)

	def test_no_email(self):
		self.data['email'] = 'notemail.com'
		res = post(self.test,self.url,self.data,self.content_type)
		data =json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid email'})
		self.assertEqual(res.status_code,406)

	def test_invalid_email(self):
		self.data['email'] = 'notmail@gmail.com'
		res = post(self.test,self.url,self.data,self.content_type)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid email or password'})
		self.assertEqual(res.status_code,406)

	def test_invalid_password(self):
		self.data['password'] = 'notpassword'
		res =post(self.test,self.url,self.data,self.content_type)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid username or password'})
		self.assertEqual(res.status_code,406)

	def test_extra_payload(self):
		self.data['extra'] = 'extra payload'
		res = post(self.test,self.url,self.data,self.content_type)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid payload'})
		self.assertEqual(res.status_code,406)

	def test_min_payload(self):
		del self.data['password'] 
		res = post(self.test,self.url,self.data,self.content_type)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid payload'})
		self.assertEqual(res.status_code,406)

	def test_valid_data(self):
		res = post(self.test,self.url,self.data,self.content_type)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data[0],{'message': 'login successful'})
		self.assertEqual(res.status_code,200)