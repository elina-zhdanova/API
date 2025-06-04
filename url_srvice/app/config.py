import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-me')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://user:password@localhost/url_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SHORT_URL_LENGTH = 8
    URL_EXPIRATION_DAYS = 1
    API_PREFIX = '/api/v1'
    
    BASIC_AUTH_REALM = 'URL Alias Service'
    SWAGGER_TITLE = 'URL Alias Service API'
    SWAGGER_UI_VERSION = '3.51.1'