import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///school.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///school.db'

config_map = {
    'development': ('development', DevelopmentConfig),
    'testing': ('testing', TestingConfig),
    'production': ('production', ProductionConfig),
    }

load_dotenv()
env = os.getenv('FLASK_ENV')
app_env = config_map.get(env, config_map['production'])
