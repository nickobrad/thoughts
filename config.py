import os

class Config:

    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    UPLOADED_PHOTOS_DEST ='app/static/profile_photos'

    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://omondii:2325@localhost/pitches'
   
class ProdConfig(Config):
    pass

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://omondii:2325@localhost/pitch_test'

class DevConfig(Config):

    UPLOADED_PHOTOS_DEST ='app/static/profile_photos'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://omondii:2325@localhost/pitches'
    DEBUG = True

config_options = {'development':DevConfig,'production':ProdConfig}