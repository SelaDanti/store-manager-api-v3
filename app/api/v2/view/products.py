from flask import request
from flask_restplus import Namespace, fields, Resource


ns_category = Namespace('category', description='Category views')
ns_products = Namespace('products', description='products views')

# routes
root = ''
category_id, product_id = '/<categoryId>', '/<productId>'

@ns_category.route(root)
class Category(Resource):
	"""
	all category view
	"""
	def post(self):
		return {'test': 'test'}

	def get(self):
		return {'test': 'test'}

@ns_category.route(category_id)
class CategoryId(Resource):
	"""
	one category views
	"""
	def get(self,categoryId):
		return {'test': 'test'}

	def delete(self,categoryId):
		return {'test': 'test'}

	def put(self,categoryId):
		return {'test': 'test'}

@ns_products.route(root)
class Products(Resource):
	"""
	all products view
	"""
	def post(self):
		return {'test': 'test'}

	def get(self):
		return {'test': 'test'}

@ns_products.route(product_id)
class ProductId(Resource):
	"""
	one product views
	"""
	def get(self,productId):
		return {'test': 'test'}

	def put(self,productId):
		return {'test': 'test'}

	def put(self,productId):
		return {'test': 'test'}