import unittest
import json

from app import create_app, create_database,set_key, destroy_tables
from .common import post


class TestActivate(unittest.TestCase):
	def setUp(self):
		create_database()
		set_key()
		self.test = create_app().test_client()
		self.content_type = 'application/json'
		self.data = {'first name': 'john', 'last name': 'doe',
		'email': 'john@gmail.com', 'password': 'password',
		'activation key': '12345'}
		self.url = 'api/v2/auth/activate'

	def tearDown(self):
		self.test = None
		self.content_type = None
		self.url = None
		self.data = None
		destroy_tables()

	def test_empty_data(self):
		self.data['first name'] = ''
		res = post(self.test,self.url,self.data,self.content_type)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'empty data set - first name'})
		self.assertEqual(res.status_code,406)

	def test_whitespace_data(self):
		self.data['first name'] = '   '
		res = post(self.test,self.url,self.data,self.content_type)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'whitespace data set - first name'})
		self.assertEqual(res.status_code,406)

	def test_not_email(self):
		self.data['email'] = 'notmail'
		res = post(self.test,self.url,self.data,self.content_type)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid email'})
		self.assertEqual(res.status_code,406)

	def test_not_activation_key(self):
		self.data['activation key'] = 'not key'
		res = post(self.test,self.url,self.data,self.content_type)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid activation key'})
		self.assertEqual(res.status_code,406)

	def test_extra_payload(self):
		self.data['extra item'] = 'something'
		res = post(self.test,self.url,self.data,self.content_type)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid payload'})
		self.assertEqual(res.status_code,406)

	def test_min_payload(self):
		del self.data['first name']
		res = post(self.test,self.url,self.data,self.content_type)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid payload'})
		self.assertEqual(res.status_code,406)

	def test_activating_twice(self):
		res = post(self.test,self.url,self.data,self.content_type)
		res = post(self.test,self.url,self.data,self.content_type)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'system is already active'})
		self.assertEqual(res.status_code,406)

	def test_valid_activation_data(self):
		res = post(self.test,self.url,self.data,self.content_type)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'message': 'super admin account activated'})
		self.assertEqual(res.status_code,201)

if __name__ == '__main__':
	unittest.main()