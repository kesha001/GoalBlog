from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

import logging
from logging.config import dictConfig



dictConfig(Config.LOGGER_CONFIG)
file_logger = logging.getLogger('file_logger')


csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object(Config)

    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"
    mail.init_app(app)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.error_handling import error_bp
    app.register_blueprint(error_bp)

    from app.user import user_bp
    app.register_blueprint(user_bp)

    from app.main import main_bp
    app.register_blueprint(main_bp)

    return app

app = create_app()
# that is a bad factory , it is for now just to make it work

file_logger.info("App configured!")

from app import models
