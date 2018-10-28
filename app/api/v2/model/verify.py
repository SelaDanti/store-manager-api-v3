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
