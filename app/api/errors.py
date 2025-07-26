from app.api import api_bp
from werkzeug.exceptions import BadRequest, HTTPException


@api_bp.errorhandler(HTTPException)
def handle_exception(e):
    return { "error": e.description }, e.code


@api_bp.errorhandler(BadRequest)
def handle_bad_request(message):
    return { "Error:" : "Bad request", "message": message }, 400