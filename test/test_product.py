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

	def test_empty_product(self):
		res = post(self.test,self.url,self.data,self.content_type,self.headers)
		data = json.loads(res.get_data().decode('UTF-8'))