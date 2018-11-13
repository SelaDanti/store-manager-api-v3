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
	DATABASE_NAME = 'd9pruu5aeui9mh'
	PASSWORD = '3243698d2ab20a9615af086b9f693c8111ed716036da5bda43b9ba8b97a2c9b1'
	USER = 'igwzrinpuwezvt'
	HOST = 'ec2-107-20-193-206.compute-1.amazonaws.com'
	PORT = 5432

app_config = {
	'testing':TestConfig,
	'development':DevelopmentConfig,
	'deploy':DeployConfig
}

