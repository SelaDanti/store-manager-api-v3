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