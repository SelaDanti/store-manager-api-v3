class Config:
	SECRET_KEY = '12345'
	DEBUG=False
	ENV='development'
	TESTING=False
	DATABASE_NAME = 'store_manager'
	USER = 'postgres'
	PASSWORD = 'python'
	HOST = 'localhost'


class TestConfig(Config):
	TESTING = True
	DATABASE_NAME = 'test'

class DevelopmentConfig(Config):
	DEBUG = True

class DeployConfig(Config):
	DEBUG = True
	DATABASE_NAME = 'de2al00c9h6tl1'
	PASSWORD = '22b586de11923087e5703b008bd521b34633db08c58088a2354ce78c426370df'
	USER = 'mtonjwucrfsnwu'
	HOST = 'ec2-184-73-222-192.compute-1.amazonaws.com'
	PORT = 5432

app_config = {
	'testing':TestConfig,
	'development':DevelopmentConfig,
	'deploy':DeployConfig
}

