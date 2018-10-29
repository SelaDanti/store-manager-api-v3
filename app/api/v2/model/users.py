from .verify import Verify
from ..util.db import fetch_activation, activate


class Users(Verify):
	def __init__(self,items):
		self.items = items

	def activate_account(self):
		items = self.items
		keys = ['first name','last name','email', 'password', 'activation key']

		if self.payload(self.items,keys) is False:
			return {'error': 'invalid payload'}, 406
		
		lists = [items['first name'],items['last name'],items['email'],
		items['password'],items['activation key']]
		
		if self.activate_payload(lists,keys) is not False:
			return self.activate_payload(lists,keys)
		else:
			fa = fetch_activation()
			if fa[1] == 'True':
				return {'error': 'system is already active'}, 406
			elif fa[0] != self.items['activation key']:
				return {'error': 'invalid activation key'}, 406
			else:
				activate()
				return {'message': 'super admin account activated'},201

