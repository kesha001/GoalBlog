from flask import Blueprint

user_bp = Blueprint('user_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

from app.user import forms, routes