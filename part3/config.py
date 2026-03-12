import os

class config:
    SECRET_KEY = os.getnev('SECRET_KEY' , 'default_secret_key')
    JWT_SECRET_KEY = 'stanisma_va_valider_son_rncp_12345!'
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}