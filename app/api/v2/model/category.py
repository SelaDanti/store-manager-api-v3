from .verify import Verify


class Category(Verify):
	"""
	class for category related operations
	"""
	def __init__(self,items):
		self.items = items

	def add_category(self):
		items = self.items
		keys = ['category name']

		if self.payload(items,keys) is not False:
			return {'error': 'invalid payload'}, 406
