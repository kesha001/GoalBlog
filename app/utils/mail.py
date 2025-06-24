import threading
from flask_mail import Message
from app import mail
from flask import current_app

def send_message(app_context, msg):
    app_context.push()
    mail.send(msg)


def send_mail_threading(subject, recipient, body=None, html=None):
    msg = Message(
        subject=subject,
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[recipient],
        body=body,
        html=html
    )
    x = threading.Thread(target=send_message, args=(current_app.app_context(),msg,))
    x.start()
    return 1