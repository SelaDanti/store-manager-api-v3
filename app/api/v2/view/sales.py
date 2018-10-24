from flask import request
from flask_restplus import Namespace, fields, Resource


ns_sales = Namespace('sales',description='Sales views')

@ns_sales.route('')
class AllSales(Resource):
	"""
	all sales views
	"""
	def get(self):
		return {'test': 'test'}

	def post(self):
		return {'test': 'test'}

@ns_sales.route('/<salesId>')
class OneSales(Resource):
	"""
	single sale views
	"""
	def get(self,salesId):
		return {'test': 'test'}
