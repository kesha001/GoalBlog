from flask import render_template
from app import app, mail, file_logger
from app.mail import send_error_mail
import traceback



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    tb = traceback.format_exc()

    file_logger.error("TRACEBACK : {}".format(tb))
    send_error_mail(e,tb)

    return render_template('500.html'), 500
