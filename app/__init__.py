from flask import Flask
from flask import request, g, current_app
from config import config_mapping, Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

from celery import Celery
import logging
from logging.handlers import TimedRotatingFileHandler, SMTPHandler

from flask_moment import Moment
from flask_babel import Babel

from elasticsearch import Elasticsearch

import os

from app.celery_utils import celery_init_app
from config import Config

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
moment = Moment()
babel = Babel()
# celery_app = Celery(__name__,
#                         broker=Config.CELERY_BROKER_URI, 
#                         backend=Config.CELERY_BACKEND_URI,
#                         include=["app.tasks"]
#                         )

def get_locale():
    translations = Config.LANGUAGES

    result = request.accept_languages.best_match(translations)
    # print(result)

    return result


def create_app(config_type='default'):
    """
    Supported config type parameters:
    default, testing
    """
    app = Flask(__name__)
    config_class = config_mapping[config_type]
    app.config.from_object(config_class)

    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app, locale_selector=get_locale)


    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.error_handling import error_bp
    app.register_blueprint(error_bp)

    from app.user import user_bp
    app.register_blueprint(user_bp)

    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    client = Elasticsearch(
        hosts=app.config['ELASTIC_SEARCH_URI']
    ) if app.config['ELASTIC_SEARCH_URI'] else None

    app.es_client = client

    app.logger.info(f"Elasticsearch client : {client}")


    if not os.path.exists('logs'):
            os.mkdir('logs')
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    file_handler = TimedRotatingFileHandler(
        filename="logs/goalblog.log",
        when='D',
        interval=1
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    celery_init_app(app)
    

    # print("Debug status: ", not int(app.debug))
    # type(app.debug) == 'str'
    if not int(app.debug):
        app.logger.info("Starting configuring smtp")
        secure=()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr=app.config['MAIL_USERNAME'],
            toaddrs=app.config['ADMINS'],
            subject='Application Error',
            credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']),
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

        app.logger.info("SMTP logging handler configured")



    app.logger.info("App configured!")

    return app


from app import models