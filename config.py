import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'my_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or \
    'sqlite:///' + os.path.join(basedir, 'app.db')


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
                'filename': 'goalblog.log',
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