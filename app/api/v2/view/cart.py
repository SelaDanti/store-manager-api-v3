from flask import request
from flask_restplus import Namespace, fields, Resource

from ..util.auth import token_required,get_user
from ..model.cart import Carts

ns_cart = Namespace('cart',description='carts views')

mod_cart = ns_cart.model('carts',{
	'product id': fields.Integer('product id'),
	'quantity': fields.Integer('quantity')
	})

@ns_cart.route('')
class CartAll(Resource):
	@token_required
	@ns_cart.doc(security='apikey')
	@ns_cart.expect(mod_cart)
	def post(self):
		data = request.get_json()
		data['user id'] = get_user()['id']
		return Carts(data).add_cart()

	@token_required
	@ns_cart.doc(security='apikey')
	def get(self):
		return {'':''}

@ns_cart.route('/<cartId>')
class CartSingle(Resource):
	@token_required
	@ns_cart.doc(security='apikey')
	def get(self):
		return {'': ''}

	@token_required
	@ns_cart.doc(security='apikey')
	def delete(self):
		return {'0':''}