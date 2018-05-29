
import logging
class Config(object):

    SECRET_KEY = 'q7pBNcWPgmF6BqB6b5VICF7z7pI+90o0O4CaJsFGjzRsYiya9SEgUDytXvzFsIaR'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI='mysql://root:mysql@127.0.0.1:3306/information_28'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = '6379'
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True

    # 设置

    PERMANENT_SESSION_LIFETIME = 60*60*1

class DConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/information_28'
    CONFIG_LEVEL = logging.DEBUG

class EConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/information_29'
    CONFIG_LEVEL = logging.ERROR

class UConfig(Config):
    TESTINg = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/information_30'
    CONFIG_LEVEL = logging.DEBUG


deta_config = {
    'd':DConfig,
    'e':EConfig,
    'u':UConfig
}