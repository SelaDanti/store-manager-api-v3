from flask import request
from flask_restplus import Namespace, fields, Resource

from ..util.auth import token_required,get_user
from ..model.cart import Carts
from ..util.cart_db import get_all_cart,convert_to_id

ns_cart = Namespace('cart',description='carts views')

mod_cart = ns_cart.model('carts',{
	'product name': fields.String('product name'),
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
		data['product id'] = convert_to_id(data['product name'])
		del data['product name']
		return Carts(data).add_cart()

	@token_required
	@ns_cart.doc(security='apikey')
	def get(self):
		return get_all_cart()

@ns_cart.route('/<productId>')
class CartSingle(Resource):
	@token_required
	@ns_cart.doc(security='apikey')
	def delete(self,productId):
		return Carts.delete_cart(productId)