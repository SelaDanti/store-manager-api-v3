from .verify import Verify
from ..util.product_db import get_one_product
from ..util.cart_db import insert_cart,decrement, already_exist


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
			return [{'error': 'invalid quantity'},
			{'hint': '{} items in inventory. {} less'.format(product[0]['quantity'],bal)}], 406
		else:
			if already_exist(self.items['product id']) is False:
				return {'':''}
			else:
				self.items['price'] = product[0]['price']
				decrement(self.items['product id'])
				insert_cart(self.items)
				return already_exist(self.items['product id'])

