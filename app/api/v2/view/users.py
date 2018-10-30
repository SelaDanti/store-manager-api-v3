from flask import request
from flask_restplus import Namespace, fields, Resource

from ..model.users import Users


ns_auth = Namespace('auth',description='Activation and Login views')
ns_attendant = Namespace('attendants', description='Attendants view')

# routes
root, attendant_id = '', '/<attendantId>'
activate, login = '/activate', '/login'

# models
mod_activate = ns_auth.model('activate',{
	'first name': fields.String('first name'),
	'last name': fields.String('last name'),
	'email': fields.String('email'),
	'password': fields.String('password'),
	'activation key': fields.String('activation key')
	})

mod_login = ns_auth.model('login',{
	'email': fields.String('email'),
	'password': fields.String('password')
	})

@ns_auth.route(login)
class Login(Resource):
	# user login views
	@ns_auth.expect(mod_login)
	def post(self):
		data = request.get_json()
		return Users(data).login()

@ns_auth.route(activate)
class ActivationKey(Resource):
	# activation of the system
	@ns_auth.expect(mod_activate)
	def post(self):
		data = request.get_json()
		return Users(data).activate_account()

@ns_attendant.route(root)
class Attendants(Resource):
	# User registration views
	def post(self):
		return {'test': 'test'}

	def get(self):
		return {'test': 'test'}

@ns_attendant.route(attendant_id)
class AttendantsId(Resource):
	# Attendants views
	def delete(self,attendantId):
		return {'test': 'test'}

	def put(self,attendantId):
		return {'test': 'test'}

	def get(self,attendantId):
		return {'test': 'test'}
