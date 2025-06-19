import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'my_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or \
    'sqlite:///' + os.path.join(basedir, 'app.db')

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    # MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL") #even if ssl = false it causes error


    LOGGER_CONFIG = {
        'version': 1,
        'formatters': {''
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            },
            'file': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': 'logs/goalblog.log',
                'when': 'D',
                'interval': 1,
                'formatter': 'default'
            }

        },
        'loggers': {    
            'file_logger': {
                'level': 'INFO',
                'handlers': ['file']
            }
        }
    }