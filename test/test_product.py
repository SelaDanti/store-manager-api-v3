import unittest
import json

from app import create_app, create_database,set_key, destroy_tables
from .common import post, create_super_admin, super_admin_token,get, put, delete, create_category


class TestActivate(unittest.TestCase):
	def setUp(self):
		create_database()
		set_key()
		self.test = create_app().test_client()
		self.content_type = 'application/json'
		self.data = {'product name': 'omo','miq':10, 'quantity': 34, "category id": 1,'uom':'packet','price':10}
		self.url = 'api/v2/products'
		create_super_admin(self.test,self.content_type)
		self.headers = {'X-API-KEY': '{}'.format(super_admin_token(self.test,self.content_type))}
		create_category(self.test,self.content_type,self.headers)

	def tearDown(self):
		self.test = None
		self.content_type = None
		self.url = None
		self.data = None
		destroy_tables()

	def test_empty_product(self):
		self.data['product name'] = ''
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'empty data set - product name'})
		self.assertEqual(res.status_code,406)

	def test_not_uom(self):
		self.data['uom'] = 'notuom'
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid uom'})
		self.assertEqual(res.status_code,406)

	def test_whitespace_product(self):
		self.data['product name'] = '  '
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'whitespace data set - product name'})
		self.assertEqual(res.status_code,406)

	def test_zero_quantity_product(self):
		self.data['quantity'] = 0
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'quantity can not be less than one'})
		self.assertEqual(res.status_code,406)

	def test_not_int_product(self):
		self.data['miq'] = 's'
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'data set - miq should be an integer'})
		self.assertEqual(res.status_code,406)

	def test_not_string_product(self):
		self.data['product name'] = 3
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'data set - product name should be a string'})
		self.assertEqual(res.status_code,406)

	def test_extra_payload(self):
		self.data['extra'] = 'extras'
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid payload'})
		self.assertEqual(res.status_code,406)

	def test_invalid_category_id(self):
		self.data['category id'] = 3
		post(self.test,self.url,self.data,self.content_type,self.headers)
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid category id'})
		self.assertEqual(res.status_code,406)

	def test_two_items_product(self):
		post(self.test,self.url,self.data,self.content_type,self.headers)
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'product already exists'})
		self.assertEqual(res.status_code,406)

	def test_add_items_product(self):
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'message': 'product omo added'})
		self.assertEqual(res.status_code,201)

	def test_update_product(self):
		post(self.test,self.url,self.data,self.content_type,self.headers)
		self.url = 'api/v2/products/{}'.format(1)
		res = put(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'message': 'product omo updated'})
		self.assertEqual(res.status_code,201)

	def test_update_product_invalid_id(self):
		self.url = 'api/v2/products/{}'.format(-74)
		res = put(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid product id'})
		self.assertEqual(res.status_code,406)


	def test_get_product(self):
		post(self.test,self.url,self.data,self.content_type,self.headers)
		self.url = 'api/v2/products/{}'.format(1)
		res = get(self.test,self.url,self.content_type,self.headers)
		self.assertEqual(res.status_code,200)

	def test_delete_product(self):
		post(self.test,self.url,self.data,self.content_type,self.headers)
		self.url = 'api/v2/products/{}'.format(1)
		res = delete(self.test,self.url,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'message': 'product deleted'})
		self.assertEqual(res.status_code,202)

if __name__ == '__main__':
	unittest.main()
