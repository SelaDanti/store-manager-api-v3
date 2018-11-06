import unittest
import json

from app import create_app, create_database,set_key, destroy_tables
from .common import post,delete, create_super_admin, super_admin_token,get, put, post_product,create_category


class TestSales(unittest.TestCase):
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
		self.assertEqual(data,{'error': {'hint': '34 items in inventory. 1 less'}}) 
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

	def test_delete_data(self):
		post(self.test,self.url,self.data,self.content_type,self.headers)
		self.url = 'api/v2/cart/{}'.format(1)
		res = delete(self.test,self.url,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data, {'message': 'product deleted'}) 
		self.assertEqual(res.status_code,202)

	def test_empty_cart(self):
		self.url = 'api/v2/sales'
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data, {'message': 'cart is empty'})
		self.assertEqual(res.status_code,404)

	def test_valid_sales(self):
		post(self.test,self.url,self.data,self.content_type,self.headers)
		self.url = 'api/v2/sales'
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data, {'message': 'sale created'})
		self.assertEqual(res.status_code,201)

	def test_get_sales(self):
		post(self.test,self.url,self.data,self.content_type,self.headers)
		self.url = 'api/v2/sales'
		post(self.test,self.url,self.data,self.content_type,self.headers)
		res = get(self.test,self.url,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(res.status_code,200)

	def test_get_one_sales(self):
		post(self.test,self.url,self.data,self.content_type,self.headers)
		self.url = 'api/v2/sales/{}'.format(1)
		post(self.test,self.url,self.data,self.content_type,self.headers)
		res = get(self.test,self.url,self.content_type,self.headers)
		self.assertEqual(res.status_code,200)

	def test_get_invalid_sales(self):
		self.url = 'api/v2/sales/{}'.format(110)
		res = get(self.test,self.url,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))
		self.assertEqual(data,{'error': 'sales not found'})
		self.assertEqual(res.status_code,404)


if __name__ == '__main__':
	unittest.main()