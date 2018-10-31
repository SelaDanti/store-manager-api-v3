from .verify import Verify

from ..util.product_db import insert_product, update_product,get_one_product, get_all_product,delete_product


class Products(Verify):
	"""
	class to for Products
	"""
	def __init__(self,items):
		self.items = items

	def add_product(self):
		if self.product_payload(self.items) is not False:
			return self.product_payload(self.items)
		else:
			return insert_product(self.items)

	def edit_product(self,id):
		if self.product_payload(self.items) is not False:
			return self.product_payload(self.items)
		if get_one_product(id)[1] == 404:
			return {'error': 'invalid product id'},406
		else:
			return update_product(self.items,id)

	@classmethod
	def get_one(self,id):
		return get_one_product(id)

	@classmethod
	def get_all(self):
		return get_all_product()

	@classmethod
	def remove(self,id):
		if get_one_product(id)[1] == 404:
			return {'error': 'invalid product id'},406
		else:
			return delete_product(id)
