from flask import request
from flask_restplus import Namespace, Resource, fields

from ..util.auth import token_required, get_user,only_attendant
from ..util.sales_db import (products, get_total,insert_new_sale,clear_cart,check_cart,get_all_sales,
	get_by_id_attendant,get_by_id_admin)


ns_sale = Namespace('sales',description='Sales Endpoints')


@ns_sale.route('')
class GetAll(Resource):
	"""
	Class contains get and post http method
	for sales record
	"""
	@token_required
	@ns_sale.doc(security='apikey')
	def get(self):
		if get_all_sales() is False:
			return {'error': 'no sales found'}, 404
		return get_all_sales()

	@token_required
	@only_attendant
	@ns_sale.doc(security='apikey')
	def post(self):
		id = int(get_user()['id'])
		total = get_total(id)
		product = products(id)
		if check_cart(id) is False:
			return {'message': 'cart is empty'},404
		else:
			clear_cart(id)
			insert_new_sale(product,total,id)
			return {'message': 'sale created'}

@ns_sale.route('/<saleId>')
class getOne(Resource):
	"""
	class contains http method get
	for getting	one sale record
	"""
	@token_required
	@ns_sale.doc(security='apikey')
	def get(self,saleId):
		if get_by_id_admin(int(saleId)) is False:
			return {'error': 'sales not found'},404

		if get_by_id_attendant(int(get_user()['id'])) is False:
			return {'error': 'sales not found'},404

		if get_user()['type'] == 'super admin' or get_user()['type'] == 'admin':
			return get_by_id_admin(int(saleId))

		else:
			return get_by_id_attendant(int(get_user()['id']))
