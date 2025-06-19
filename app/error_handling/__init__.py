from flask import Blueprint

error_bp = Blueprint('error_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

from app.error_handling import errors