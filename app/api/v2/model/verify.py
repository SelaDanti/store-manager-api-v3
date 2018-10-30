import re


class Verify:
	"""
	class to verify data
	"""
	def is_empty(self,items,keys):
		for item in items:
			if bool(item) is False:
				return {'error': 'empty data set - {}'.format(keys[items.index(item)])},406
				break
		return False

	def is_whitespace(self,items,keys):
		for item in items:
			if item.isspace() is True:
				return {'error': 'whitespace data set - {}'.format(keys[items.index(item)])},406
				break
		return False

	def is_string(self,items,keys):
		for item in items:
			if type(item) != str:
				return {'error': 'data set - {} should be a string'.format(keys[items.index(item)])},406
				break
		return False

	def is_number(self,items,keys):
		for item in items:
			if type(item) != int and type(item) != float:
				return {'error': 'data set - {} should be an integer'.format(keys[items.index(item)])},406
				break
		return False

	def payload(self,items,keys):
		items = items.keys()
		if len(items) == len(keys):
			for item in items:
				if item not in keys:
					return False
			return True
		else:
			return False

	def is_email(self,email):
		result = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
		if result is None:
			res = False
		else:
			res = True
		return res

	def activate_payload(self,items,keys):
		if self.is_string(items,keys) is not False:
			return self.is_string(items,keys)
		elif self.is_empty(items,keys) is not False:
			return self.is_empty(items,keys)
		elif self.is_whitespace(items,keys) is not False:
			return self.is_whitespace(items,keys)
		elif self.is_email(items[2]) is False:
			return {'error': 'invalid email'}, 406
		else:
			return False


	def login_payload(self,items,keys):
		if self.is_string(items,keys) is not False:
			return self.is_string(items,keys)
		elif self.is_empty(items,keys) is not False:
			return self.is_empty(items,keys)
		elif self.is_whitespace(items,keys) is not False:
			return self.is_whitespace(items,keys)
		elif self.is_email(items[0]) is False:
			return {'error': 'invalid email'}, 406
		else:
			return False

	def attendant_payload(self,items,keys):
		if self.is_string(items,keys) is not False:
			return self.is_string(items,keys)
		elif self.is_empty(items,keys) is not False:
			return self.is_empty(items,keys)
		elif self.is_whitespace(items,keys) is not False:
			return self.is_whitespace(items,keys)
		elif self.is_email(items[2]) is False:
			return {'error': 'invalid email'}, 406
		elif items[3] != 'admin' and items[3] != 'attendant':
			return {'error': 'invalid role'}, 406
		else:
			return False