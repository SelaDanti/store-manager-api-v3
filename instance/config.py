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

app_config = {
	'testing':TestConfig,
	'development':DevelopmentConfig
}

