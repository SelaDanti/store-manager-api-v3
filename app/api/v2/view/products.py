from flask import request
from flask_restplus import Namespace, fields, Resource

from ..util.auth import token_required
from ..model.category import Categories

ns_category = Namespace('category', description='Category views')
ns_products = Namespace('products', description='products views')

mod_category = ns_category.model('category',{
	'category name': fields.String('category name')
	})

# routes
root = ''
category_id, product_id = '/<categoryId>', '/<productId>'

@ns_category.route(root)
class Category(Resource):
	# all category view
	@ns_category.expect(mod_category)
	@token_required
	@ns_category.doc(security='apikey')
	def post(self):
		data = request.get_json()
		return Categories(data).add_category()

	@token_required
	@ns_category.doc(security='apikey')
	def get(self):
		return Categories.get_all()

@ns_category.route(category_id)
class CategoryId(Resource):
	# one category views
	@token_required
	@ns_category.doc(security='apikey')
	def get(self,categoryId):
		return Categories.get_one(categoryId)

	@ns_category.expect(mod_category)
	@token_required
	@ns_category.doc(security='apikey')
	def put(self,categoryId):
		return {'test': 'test'}

@ns_products.route(root)
class Products(Resource):
	# all products view
	def post(self):
		return {'test': 'test'}

	def get(self):
		return {'test': 'test'}

@ns_products.route(product_id)
class ProductId(Resource):
	# one product views
	def get(self,productId):
		return {'test': 'test'}

	def put(self,productId):
		return {'test': 'test'}

	def put(self,productId):
		return {'test': 'test'}