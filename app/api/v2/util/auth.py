import jwt

from functools import wraps
from flask import request



def token_required(f):
	@wraps(f)
	def decorated(*arg,**kwargs):
		token = None
		if 'X-API-KEY' in request.headers:
			token = request.headers['X-API-KEY']
		if not token:
			return {'error': 'token is missing'},401
		try:
			token = jwt.decode(token,'12345',algorithms=['HS256'])
		except:
			return {'error': 'token is invalid'},401
		return f(*arg,**kwargs)
	return decorated


def only_admin(f):
	@wraps(f)
	def decorated(*arg,**kwargs):
		token = request.headers['X-API-KEY']
		token = jwt.decode(token,'12345',algorithms=['HS256'])
		if token['type'] != 'super admin' and token['type'] != 'admin':
			return {'error':'This endpoint is only accessible to admin'}, 401
		return f(*arg,**kwargs)
	return decorated

def only_attendant(f):
	@wraps(f)
	def decorated(*arg,**kwargs):
		token = request.headers['X-API-KEY']
		token = jwt.decode(token,'12345',algorithms=['HS256'])
		if token['type'] != 'super admin' and token['type'] != 'attendant':
			return {'error':'This endpoint is only accessible to store attendant'}, 401
		return f(*arg,**kwargs)
	return decorated