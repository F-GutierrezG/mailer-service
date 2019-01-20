import os


class BaseConfig:
    """ Base configuration """
    TESTING = False
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    BCRYPT_LOG_ROUNDS = 13


class DevelopmentConfig(BaseConfig):
    """ Development configuration """
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    """ Testing configuration """
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    BCRYPT_LOG_ROUNDS = 4


class StagingConfig(BaseConfig):
    """ Staging configuration """
    pass


class ProductionConfig(BaseConfig):
    """ Production configuration """
    DEBUG = False
