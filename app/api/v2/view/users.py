from flask import request
from flask_restplus import Namespace, fields, Resource


ns_auth = Namespace('auth',description='Activation and Login views')
ns_attendant = Namespace('attendants', description='Attendants view')

# routes
root, attendant_id = '', '/<attendantId>'
activate, login = '/activate', '/login'

@ns_auth.route(login)
class Login(Resource):
	"""
	user login views
	"""
	def post(self):
		return [{'test':'test'},{'token': ''}]

@ns_auth.route(activate)
class ActivationKey(Resource):
	"""
	activation of the system
	"""
	def post(self):
		return {'test': 'test'}

@ns_attendant.route(root)
class Attendants(Resource):
	"""
	User registration views
	"""
	def post(self):
		return {'test': 'test'}

	def get(self):
		return {'test': 'test'}

@ns_attendant.route(attendant_id)
class AttendantsId(Resource):
	"""
	Attendants views
	"""
	def delete(self,attendantId):
		return {'test': 'test'}

	def put(self,attendantId):
		return {'test': 'test'}

	def get(self,attendantId):
		return {'test': 'test'}
