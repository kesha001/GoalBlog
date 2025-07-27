from flask import render_template, request
from app.error_handling import error_bp
from app.api.errors import error_response as api_error_response


def client_wants_json():
    return True if request.accept_mimetypes.accept_json \
    else False

@error_bp.app_errorhandler(404)
def page_not_found(e):
    if client_wants_json():
        return api_error_response(404)
    return render_template('error_handling/404.html'), 404

@error_bp.app_errorhandler(500)
def internal_server_error(e):
    if client_wants_json():
        return api_error_response(500)
    return render_template('error_handling/500.html'), 500