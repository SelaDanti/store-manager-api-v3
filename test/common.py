import json

def post(test,url,data,content_type,header=None):
	response = test.post(url,content_type=content_type,
		data=json.dumps(data),headers=header)
	return response

def put(test,url,data,content_type,header=None):
	response = test.put(url,content_type=content_type,
		data=json.dumps(data),headers=header)
	return response

def get(test,url,content_type,header=None):
	response = test.get(url,content_type=content_type,headers=header)
	return response

def delete(test,url,content_type,header=None):
	response = test.delete(url,content_type=content_type,headers=header)
	return response

def create_super_admin(test,content_type):
	data = {'first name': 'john', 'last name': 'doe',
		'email': 'john@gmail.com', 'password': 'password',
		'activation key': '12345'}
	url = 'api/v2/auth/activate'
	res = post(test,url,data,content_type)
	if res.status_code == 201:
		return 'OK' 
	else:
		return json.loads(res.get_data().decode('UTF-8'))


def super_admin_token(test,content_type):
	data = {'email': 'john@gmail.com', 'password': 'password'}
	url = 'api/v2/auth/login'
	res = post(test,url,data,content_type)
	data = json.loads(res.get_data().decode('UTF-8'))
	return data[1]['token']


def create_category(test,content_type,headers=None):
	data = {'category name': 'soaps'}
	url = 'api/v2/category'
	post(test,url,data,content_type,headers)

def post_product(test,content_type,headers):
	url = 'api/v2/products'
	data = {'product name': 'omo','miq':10, 'quantity': 34, "category id": 1,'uom':'packet','price':100}
	post(test,url,data,content_type,headers)
		

if __name__ == '__main__':
	unittest.main()
