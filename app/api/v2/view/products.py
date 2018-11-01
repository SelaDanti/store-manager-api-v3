from flask import request
from flask_restplus import Namespace, fields, Resource

from ..util.auth import token_required
from ..model.category import Categories
from ..model.product import Products

ns_category = Namespace('category', description='Category views')
ns_products = Namespace('products', description='products views')

mod_category = ns_category.model('category',{
	'category name': fields.String('category name')
	})

mod_product = ns_products.model('products',{
	'product name': fields.String('category name'),
	'quantity': fields.Integer('qauntity'),
	'miq': fields.Integer('miq'),
	'category id': fields.Integer('category id'),
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
	def post(self):
		data =request.get_json()
		return Products(data).add_product()

	@token_required
	@ns_category.doc(security='apikey')
	def get(self):
		return Products.get_all()

@ns_products.route(product_id)
class ProductId(Resource):
	# one product views
	@token_required
	@ns_products.doc(security='apikey')
	def get(self,productId):
		return Products.get_one(productId)

	@token_required
	@ns_products.doc(security='apikey')
	def delete(self,productId):
		return Products.remove(productId)	

	@token_required
	@ns_products.doc(security='apikey')
	@ns_products.expect(mod_product)
	def put(self,productId):
		data = request.get_json()
		return Products(data).edit_product(productId)