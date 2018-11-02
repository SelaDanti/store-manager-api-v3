from flask import request
from flask_restplus import Namespace, fields, Resource

from ..model.users import Users
from ..util.auth import token_required

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

mod_attendant = ns_attendant.model('attendant',{
	'first name': fields.String('first name'),
	'last name': fields.String('last name'),
	'email': fields.String('email'),
	'password': fields.String('password'),
	'role': fields.String('role')
	})
mod_role = ns_attendant.model('edit attendant',{
	'user type': fields.String('Type of user')
	})

@ns_auth.route(login)
class Login(Resource):
	# user login views
	@ns_auth.expect(mod_login)
	def post(self):
		data = request.get_json()
		data['email'] = data['email'].lower() 
		return Users(data).login()

@ns_auth.route(activate)
class ActivationKey(Resource):
	# activation of the system
	@ns_auth.expect(mod_activate)
	def post(self):
		data = request.get_json()
		data['email'] = data['email'].lower() 
		return Users(data).activate_account()

@ns_attendant.route(root)
class Attendants(Resource):
	# User registration views
	@ns_attendant.expect(mod_attendant)
	@ns_attendant.doc(security='apikey')
	@token_required
	def post(self):
		data = request.get_json()
		return Users(data).add_attendant()

	@ns_attendant.doc(security='apikey')
	@token_required
	def get(self):
		return Users.get_attendants()

@ns_attendant.route(attendant_id)
class AttendantsId(Resource):
	# Attendants views
	@token_required
	@ns_attendant.expect(mod_role)
	@ns_attendant.doc(security='apikey')
	def put(self,attendantId):
		data = request.get_json()
		return Users(data).update_user_type(attendantId)

	@ns_attendant.doc(security='apikey')
	@token_required
	def get(self,attendantId):
		return Users.get_one_attendant(attendantId)
