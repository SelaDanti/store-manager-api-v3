import json

def post(test,url,data,content_type):
	response = test.post(url,content_type=content_type,
		data=json.dumps(data))
	return response

def put(url,data,content_type):
	pass

def get(url,content_type):
	pass

def delete(url,content_type):
	pass

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