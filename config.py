import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    APP_NAME = "Uni Ninja"
    SECRET_KEY = 'just a test string for now, change later'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    OAUTHLIB_INSECURE_TRANSPORT = 1
    SQLALCHEMY_DATABASE_URI = 'postgres://mwbmjfsrxqwulo:5c962ac9681facb8459cd7be573dcfc4262a4e10d2ba8d989f5dcae100a8b0d6@ec2-54-243-252-91.compute-1.amazonaws.com:5432/d2hdijpk4h5m4v'


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = True


config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig
}
