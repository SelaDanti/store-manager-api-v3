from .verify import Verify

from ..util.category_db import insert_category, category_name_exist,all_categories, one_category, delete, update


class Categories(Verify):
	"""
	class for category related operations
	"""
	def __init__(self,items):
		self.items = items

	def add_category(self):
		items = self.items
		keys = ['category name']

		if self.payload(items,keys) is False:
			return {'error': 'invalid payload'}, 406

		lists = [items['category name'].lower()]

		if self.category_payload(lists,keys) is not False:
			return self.category_payload(lists,keys)
		else:
			if category_name_exist(items['category name'].lower()) is not True:
				return category_name_exist(items['category name'].lower())
			else:
				return insert_category(items['category name'].lower())

	@classmethod
	def get_all(cls):
		return all_categories()

	@classmethod
	def get_one(cls,categoryId):
		return one_category(categoryId)

	@classmethod
	def delete_category(cls,categoryId):
		if one_category(categoryId)[1] == 404:
			return {'error': 'invalid id'},406
		else:
			return delete(categoryId)

	@classmethod
	def update_catogory(cls,categoryId,items):
		if one_category(categoryId)[1] == 404:
			return {'error': 'invalid id'},406
		else:
			return update(categoryId,items['category name'])


