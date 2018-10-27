from flask import request
from flask_restplus import Namespace, fields, Resource


ns_user = Namespace('auth',description='Auth views')
ns_attendant = Namespace('attendants', description='edit attendants views')

@ns_user.route('/login')
class Login(Resource):
	"""
	user login views
	"""
	def post(self):
		return [{'test':'test'},{'token': ''}]


@ns_user.route('/register')
class Register(Resource):
	"""
	User registration views
	"""
	def post(self):
		return {'test': 'test'}

@ns_user.route('/activate')
class ActivationKey(Resource):
	"""
	activation of the system
	"""
	def post(self):
		return {'test': 'test'}

@ns_attendant.route('')
class Attendants(Resource):
	"""
	All attendants views
	"""
	def get(self):
		return {'test get all': 'test'}

@ns_attendant.route('/<attendantId>')
class GetOneAttendant(Resource):
	"""
	Get one attendant view
	"""
	def get(self,attendantId):
		return {'test': 'test'}

	def put(self,attendantId):
		return {'test': 'test'}

	def delete(self,attendantId):
		return {'test': 'test'}