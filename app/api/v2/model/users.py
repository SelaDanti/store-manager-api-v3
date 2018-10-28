from .verify import Verify


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
			return items