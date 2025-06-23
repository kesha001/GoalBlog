import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    
    TESTING = False
    DEBUG = os.environ.get('FLASK_DEBUG') or False

    SECRET_KEY = os.environ.get("SECRET_KEY") or 'my_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or \
    'sqlite:///' + os.path.join(basedir, 'app.db')

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    # MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL") #even if ssl = false it causes error
    ADMINS = ['berdstudy@gmail.com']

    GOALS_PER_PAGE = 5


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI") or \
    'sqlite:///' + os.path.join(basedir, 'test.db')
    WTF_CSRF_ENABLED = False


config_mapping = {
    'default': 'config.Config',
    'testing': 'config.TestingConfig'
}