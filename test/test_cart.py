import unittest
import json

from app import create_app, create_database,set_key, destroy_tables
from .common import post, create_super_admin, super_admin_token,get, put, post_product,create_category


class TestActivate(unittest.TestCase):
	def setUp(self):
		create_database()
		set_key()
		self.test = create_app().test_client()
		self.content_type = 'application/json'
		self.data = {'quantity': 2,'product id': 1
}
		self.url = 'api/v2/cart'
		create_super_admin(self.test,self.content_type)
		self.headers = {'X-API-KEY': '{}'.format(super_admin_token(self.test,self.content_type))}
		create_category(self.test,self.content_type,self.headers)
		post_product(self.test,self.content_type,self.headers)

	def tearDown(self):
		self.test = None
		self.content_type = None
		self.url = None
		self.data = None
		destroy_tables()

	def test_not_number(self):
		self.data['quantity'] = 's'
		res=post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'data set - quantity should be an integer'}) 
		self.assertEqual(res.status_code,406)

	def test_invalid_payload(self):
		self.data['extra'] = ''
		res=post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid payload'}) 
		self.assertEqual(res.status_code,406)


	def test_quantity_less_than_zero(self):
		self.data['quantity'] = 0
		res=post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'quantity can not be less than one'}) 
		self.assertEqual(res.status_code,406)

	def test_min_payload(self):
		del self.data['quantity']
		res=post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'invalid payload'}) 
		self.assertEqual(res.status_code,406)

	def test_invalid_product_id(self):
		self.data['product id'] = -243
		res=post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data, {'error': 'product not found'}) 
		self.assertEqual(res.status_code,404)

	def test_invalid_quantity(self):
		self.data['quantity'] = 35
		res=post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,[{'error': 'invalid quantity'},{'hint': '34 items in inventory. 1 less'}]) 
		self.assertEqual(res.status_code,406)

	def test_posting_twice(self):
		post(self.test,self.url,self.data,self.content_type,self.headers)
		res=post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'message': 'quantity of id 1 incremented to 3'}) 
		self.assertEqual(res.status_code,201)

	def test_valid_data(self):
		res=post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'message': 'product added to cart'}) 
		self.assertEqual(res.status_code,201)


if __name__ == '__main__':
	unittest.main()