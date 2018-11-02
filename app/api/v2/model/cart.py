from .verify import Verify
from ..util.product_db import get_one_product
from ..util.cart_db import insert_cart,decrement, already_exist,increment, get_cart_item,revert_back,delete_cart


class Carts(Verify):
	def __init__(self,items):
		self.items =items

	def add_cart(self):
		product = get_one_product(self.items['product id'])
		if self.cart_payload(self.items) is not False:
			return self.cart_payload(self.items)
		elif product[1] == 404:
			return product
		elif product[0]['quantity'] < self.items['quantity']:
			bal = self.items['quantity'] - product[0]['quantity']
			return {'error': {'hint': '{} items in inventory. {} less'.format(product[0]['quantity'],bal)}}, 406
		else:
			if already_exist(self.items['product id']) is False:
				decrement(self.items['product id'],self.items['quantity'])
				return increment(self.items['product id'])
			else:
				self.items['price'] = product[0]['price']
				decrement(self.items['product id'],self.items['quantity'])
				return insert_cart(self.items)

	@classmethod
	def delete_cart(cls,id):
		try:
			product_quantity = get_one_product(id)[0]['quantity']
			cart_quantity = get_cart_item(id)[0]['quantity']
			q = product_quantity + cart_quantity
			delete_cart(id)
			revert_back(q,id)
			return {'message':'product deleted'}, 202
		except KeyError:
			return {'error': 'invalid key'},406


