import unittest
import json

from app import create_app, create_database,set_key, destroy_tables
from .common import post, create_super_admin, super_admin_token,get, put, delete


class TestActivate(unittest.TestCase):
	def setUp(self):
		create_database()
		set_key()
		self.test = create_app().test_client()
		self.content_type = 'application/json'
		self.data = {'category name': 'soaps'}
		self.url = 'api/v2/category'
		create_super_admin(self.test,self.content_type)
		self.headers = {'X-API-KEY': '{}'.format(super_admin_token(self.test,self.content_type))}

	def tearDown(self):
		self.test = None
		self.content_type = None
		self.url = None
		self.data = None
		destroy_tables()


	def test_empty_data(self):
		self.data['category name'] = ''
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'empty data set - category name'})
		self.assertEqual(res.status_code,406)

	def test_whitespace_data(self):
		self.data['category name'] = '  '
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error':'whitespace data set - category name'})
		self.assertEqual(res.status_code,406)

	def test_extra_payload(self):
		self.data['extra'] = 'extra'
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid payload'})
		self.assertEqual(res.status_code,406)

	def test_valid_data(self):
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'message': 'categort added'})
		self.assertEqual(res.status_code,201)

	def test_get_non_categories(self):
		res = get(self.test,self.url,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'no record found'})
		self.assertEqual(res.status_code,404)

	def test_get_categories(self):
		post(self.test,self.url,self.data,self.content_type,self.headers)
		res = get(self.test,self.url,self.content_type,self.headers)
		self.assertEqual(res.status_code,200)

	def test_get_invalid_category_id(self):
		self.url = 'api/v2/category/{}'.format(23)
		res = get(self.test,self.url,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'no record found'})
		self.assertEqual(res.status_code,404)

	def test_get_valid_category_id(self):
		post(self.test,self.url,self.data,self.content_type,self.headers)
		self.url = 'api/v2/category/{}'.format(1)
		res = get(self.test,self.url,self.content_type,self.headers)
		self.assertEqual(res.status_code,200)

	def test_delete_category_not_exits(self):
		self.url = 'api/v2/category/{}'.format(11)
		res = delete(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid id'})
		self.assertEqual(res.status_code,406)

	def test_delete_cateory(self):
		post(self.test,self.url,self.data,self.content_type,self.headers)
		self.url = 'api/v2/category/{}'.format(1)
		res = delete(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'message': 'record deleted'})
		self.assertEqual(res.status_code,201)

	def test_update_category(self):
		self.url = 'api/v2/category/{}'.format(11)
		res = put(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid id'})
		self.assertEqual(res.status_code,406)

	def test_update_category_invalid_id(self):
		self.url = 'api/v2/category/{}'.format(31)
		res = put(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid id'})
		self.assertEqual(res.status_code,406)

	def test_update_category(self):
		post(self.test,self.url,self.data,self.content_type,self.headers)
		self.url = 'api/v2/category/{}'.format(1)
		res = put(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'message': 'category name updated'})
		self.assertEqual(res.status_code,201)


if __name__ == '__main__':
	unittest.main()