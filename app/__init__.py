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

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "login"
mail = Mail(app)


file_logger.info("App configured!")

from app import routes, forms, models, errors