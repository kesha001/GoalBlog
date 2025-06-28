from flask import Flask
from flask import request, g, current_app
from config import config_mapping, Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

import logging
from logging.handlers import TimedRotatingFileHandler, SMTPHandler

from flask_moment import Moment
from flask_babel import Babel

import os


csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
moment = Moment()
babel = Babel()

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
    # print("BABEL_TRANSLATION_DIRECTORIES -- ", app.config['BABEL_TRANSLATION_DIRECTORIES'])

    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.error_handling import error_bp
    app.register_blueprint(error_bp)

    from app.user import user_bp
    app.register_blueprint(user_bp)

    from app.main import main_bp
    app.register_blueprint(main_bp)


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

    if not app.debug:
        secure=()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr=app.config['MAIL_USERNAME'],
            toaddrs=['berdstudy@gmail.com'],
            subject='Application Error',
            credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']),
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


    app.logger.info("App configured!")

    return app


from app import models