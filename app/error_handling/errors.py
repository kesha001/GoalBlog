from flask import render_template
from app import file_logger
from app.utils.mail import send_error_mail
import traceback

from app.error_handling import error_bp


@error_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('error_handling/404.html'), 404

@error_bp.app_errorhandler(500)
def internal_server_error(e):
    tb = traceback.format_exc()

    file_logger.error("TRACEBACK : {}".format(tb))
    send_error_mail(e,tb)

    return render_template('error_handling/500.html'), 500