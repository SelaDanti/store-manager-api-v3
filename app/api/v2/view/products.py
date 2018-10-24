from flask import request
from flask_restplus import Namespace, fields, Resource


ns_products = Namespace('product',description='Products views')
ns_categories = Namespace('category',description='Category views')

@ns_products.route('')
class ALlProducts(Resource):
	"""
	all products view
	"""
	def get(self):
		return {'test': 'test'}

	def post(self):
		return {'test': 'test'}

@ns_products.route('<productId>')
class Onesale(Resource):
	"""
	single product views
	"""
	def get(self,productId):
		return {'test': 'test'}


@ns_categories.route('')
class AllCategory(Resource):
	"""
	all categories view
	"""
	def get(self):
		return {'test': 'test'}

	def post(self):
		return {'test': 'test'}


@ns_categories.route('/<categoryId>')
class OneCategory(Resource):
	"""
	single category viewsss
	"""
	def get(self,categoryId):
		return {'test': 'test'}

	def get(self,categoryId):
		return {'test': 'test'}

	def put(self,categoryId):
		return {'test': 'test'}

	def delete(self,categoryId):
		return {'test': 'test'}
