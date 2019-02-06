import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    APP_NAME = "Uni Ninja"
    SECRET_KEY = 'just a test string for now, change later'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    OAUTHLIB_INSECURE_TRANSPORT = 1
    SQLALCHEMY_DATABASE_URI = 'DROPIN_URL'


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = True


config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig
}
