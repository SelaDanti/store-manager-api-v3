from flask import request
from flask_restplus import Namespace, fields, Resource

from ..util.auth import token_required,only_admin
from ..model.category import Categories
from ..model.product import Products
from ..util.category_db import all_categories, one_category, convert_to_id
from ..util.product_db import get_one_product,get_all_product

ns_category = Namespace('category', description='Category views')
ns_products = Namespace('products', description='products views')

mod_category = ns_category.model('category',{
	'category name': fields.String('category name')
	})

mod_product = ns_products.model('products',{
	'product name': fields.String('category name'),
	'quantity': fields.Integer('qauntity'),
	'miq': fields.Integer('miq'),
	'category name': fields.String('category name'),
	'uom': fields.String('uom'),
	'price': fields.Integer('price')
	})


# routes
root = ''
category_id, product_id = '/<categoryId>', '/<productId>'

@ns_category.route(root)
class Category(Resource):
	# all category view
	@ns_category.expect(mod_category)
	@token_required
	@only_admin
	@ns_category.doc(security='apikey')
	def post(self):
		data = request.get_json()
		return Categories(data).add_category()

	@token_required
	@ns_category.doc(security='apikey')
	def get(self):
		return all_categories()

@ns_category.route(category_id)
class CategoryId(Resource):
	# one category views
	@token_required
	@ns_category.doc(security='apikey')
	def get(self,categoryId):
		return one_category(categoryId)

	@ns_category.expect(mod_category)
	@token_required
	@only_admin
	@ns_category.doc(security='apikey')
	def put(self,categoryId):
		data = request.get_json()
		return Categories.update_catogory(categoryId,data)

	@token_required
	@ns_category.doc(security='apikey')
	def delete(self,categoryId):
		return Categories.delete_category(categoryId)

@ns_products.route(root)
class NewProducts(Resource):
	# all products view
	@token_required
	@ns_products.expect(mod_product)
	@ns_products.doc(security='apikey')
	@only_admin
	def post(self):
		data =request.get_json()
		cat_id = convert_to_id(data['category name'])
		data['category id'] = cat_id
		del data['category name']
		return Products(data).add_product()

	@token_required
	@ns_category.doc(security='apikey')
	def get(self):
		return get_all_product()

@ns_products.route(product_id)
class ProductId(Resource):
	# one product views
	@token_required
	@ns_products.doc(security='apikey')
	def get(self,productId):
		try:
			return get_one_product(productId)
		except KeyError:
			return {'error': 'please insert a number in the url'}

	@token_required
	@only_admin
	@ns_products.doc(security='apikey')
	def delete(self,productId):
		try:
			return Products.remove(productId)	
		except KeyError:
			return {'error': 'please insert a number in the url'}

	@token_required
	@only_admin
	@ns_products.doc(security='apikey')
	@ns_products.expect(mod_product)
	def put(self,productId):
		try:
			data = request.get_json()
			cat_id = convert_to_id(data['category name'])
			data['category id'] = cat_id
			del data['category name']
			return Products(data).edit_product(productId)
		except KeyError:
			return {'error': 'please insert a number in the url'}