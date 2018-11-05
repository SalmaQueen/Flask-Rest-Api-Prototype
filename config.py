import os
import platform


class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PLATFORM = platform.node()
    JWT_AUTH_URL_RULE = '/login'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    basedir = os.path.abspath(os.path.dirname(__file__))
    TEMPLATES_AUTO_RELOAD = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app-dev.sqlite')


class TestingConfig(Config):
    basedir = os.path.abspath(os.path.dirname(__file__))
    TEMPLATES_AUTO_RELOAD = True
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app-test.sqlite')


class ProductionConfig(Config):
    basedir = os.path.abspath(os.path.dirname(__file__))
    TEMPLATES_AUTO_RELOAD = True
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app-prod.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
