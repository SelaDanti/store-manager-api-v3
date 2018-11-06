import unittest
import json

from app import create_app, create_database,set_key, destroy_tables
from .common import post, create_super_admin, super_admin_token,get, put


class TestAttendant(unittest.TestCase):
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
		self.assertEqual(res.status_code,200)

	def test_get_one_invalid_attendant(self):
		self.url = 'api/v2/attendants/{}'.format(14)
		post(self.test,self.url,self.data,self.content_type,self.headers)
		res = get(self.test,self.url,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'message': 'record not found'})
		self.assertEqual(res.status_code,404)

	def test_letter_id(self):
		self.url = 'api/v2/attendants/{}'.format('x')
		post(self.test,self.url,self.data,self.content_type,self.headers)
		res = get(self.test,self.url,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid id'})
		self.assertEqual(res.status_code,406)

	def test_get_one_attendant(self):
		self.url = 'api/v2/attendants/{}'.format(1)
		post(self.test,self.url,self.data,self.content_type,self.headers)
		res = get(self.test,self.url,self.content_type,self.headers)
		self.assertEqual(res.status_code,200)

	def test_update_invalid_id(self):
		self.url = 'api/v2/attendants/{}'.format(2)
		self.data = {'user type': 'not user type'}
		post(self.test,self.url,self.data,self.content_type,self.headers)
		res = put(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid user type'})
		self.assertEqual(res.status_code,406)

	def test_update_invalid_payload(self):
		self.url = 'api/v2/attendants/{}'.format(2)
		self.data = {'user type': 'not user type','extra': ''}
		post(self.test,self.url,self.data,self.content_type,self.headers)
		res = put(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid payload'})	
		self.assertEqual(res.status_code,406)

	def test_update_id_not_found(self):
		self.url = 'api/v2/attendants/{}'.format(21)
		self.data = {'user type': 'admin'}
		post(self.test,self.url,self.data,self.content_type,self.headers)
		res = put(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'message': 'record not found'})	
		self.assertEqual(res.status_code,404)

	def test_update_super_admin(self):
		post(self.test,self.url,self.data,self.content_type,self.headers)
		self.url = 'api/v2/attendants/{}'.format(1)
		self.data = {'user type': 'admin'}
		res = put(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'cannot edit super admin'})	
		self.assertEqual(res.status_code,406)

	def test_update_valid_data(self):
		post(self.test,self.url,self.data,self.content_type,self.headers)
		self.data = {'user type': 'admin'}
		self.url = 'api/v2/attendants/{}'.format(2)
		res = put(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'message': 'User type change to admin'})	
		self.assertEqual(res.status_code,201)

	
if __name__ == '__main__':
	unittest.main()