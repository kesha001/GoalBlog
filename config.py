import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir in Config: ", basedir)

class Config:
    
    TESTING = False
    DEBUG = os.environ.get('FLASK_DEBUG') or False

    SECRET_KEY = os.environ.get("SECRET_KEY") or 'my_secret_key'
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/goalblogdb"
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or \
    'sqlite:///' + os.path.join(basedir, 'app.db')

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    # MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL") #even if ssl = false it causes error
    ADMINS = os.environ.get("ADMIN_EMAIL")

    GOALS_PER_PAGE = 5

    RESET_TOKEN_MAX_AGE = 3600

    LANGUAGES = ['en', 'no', 'uk']

    ELASTIC_SEARCH_URI = os.environ.get("ELASTIC_SEARCH_URI")

    CELERY_BROKER_URI = os.environ.get("CELERY_BROKER_URI") or "amqp://localhost"
    # CELERY_BACKEND_URI = "rpc://localhost"
    CELERY_BACKEND_URI = os.environ.get("CELERY_BACKEND_URI") or "redis://localhost"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI") or \
    'sqlite:///' + os.path.join(basedir, 'test.db')
    WTF_CSRF_ENABLED = False


config_mapping = {
    'default': 'config.Config',
    'testing': 'config.TestingConfig'
}