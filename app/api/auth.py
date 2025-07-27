from app.api import api_bp
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app import db
import sqlalchemy as sa
from app.models import User
from app.api.errors import error_response


user_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@user_auth.verify_password
def verify_password(username, password):
    user = db.session.scalar(sa.Select(User).where(User.username==username))

    if not user:
        return None

    if not user.check_password(password):
        return None
        
    return user


@token_auth.verify_token
def verify_token(token):
    if not token:
        return None
    return User.check_token(token)



@user_auth.error_handler
def auth_error(status):
    return error_response(status)

@token_auth.error_handler
def auth_error(status):
    return error_response(status)