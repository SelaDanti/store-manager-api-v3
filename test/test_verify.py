import unittest

from app.api.v2.model.verify import Verify


class TestVerify(unittest.TestCase):
	def setUp(self):
		self.obj = Verify()

	def tearDown(self):
		self.obj = None

	def test_is_empty(self):
		test = self.obj.is_empty(['s',''],['name','name2'])
		self.assertEqual(test,({'error': 'empty data set - name2'},406))

	def test_not_empty(self):
		test = self.obj.is_empty(['s','s'],['name','name2'])
		self.assertFalse(test)

	def test_is_whitespace(self):
		test = self.obj.is_whitespace(['s','  '],['name','name2'])
		self.assertEqual(test,({'error': 'whitespace data set - name2'},406))

	def test_not_empty(self):
		test = self.obj.is_whitespace(['s','s'],['name','name2'])
		self.assertFalse(test)

	def test_not_payload(self):
		data = {'name':'','emails': ''}
		test = self.obj.payload(data,['name','email'])
		self.assertFalse(test)

	def test_extra_payload(self):
		data = {'name':'','email':'','extra':''}
		test = self.obj.payload(data,['name','email'])
		self.assertFalse(test)

	def test_min_payload(self):
		data ={'name':''}
		test = self.obj.payload(data,['name','email'])
		self.assertFalse(test)

	def test_payload(self):
		data = {'name':'','email': ''}
		test = self.obj.payload(data,['name','email'])
		self.assertTrue(test)

	def test_not_email(self):
		test = self.obj.is_email('notmail.com')
		self.assertFalse(test)

	def test_is_mail(self):
		test = self.obj.is_email('mail@mail.com')
		self.assertTrue(test)

	def test_is_string(self):
		test = self.obj.is_string(['da',2],['name','name2'])
		self.assertEqual(test,({'error': 'data set - name2 should be a string'}, 406))

	def test_is_not_number(self):
		test = self.obj.is_number([2.4,'2'],['name','name2'])
		self.assertEqual(test,({'error': 'data set - name2 should be an integer'}, 406))

	def test_is_number(self):
		test = self.obj.is_number([2.4,2],['name','name2'])
		self.assertFalse(test)


if __name__ == '__main__':
	unittest.main()