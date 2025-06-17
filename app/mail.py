import threading
from flask_mail import Message
from app import app, mail

def send_message(app_context, msg):
    app_context.push()
    mail.send(msg)


def send_error_mail(e, tb):
    msg = Message(
        subject=e.description,
        sender=app.config['MAIL_USERNAME'],
        recipients=["berdstudy@gmail.com"],
        body=tb,
    )
    x = threading.Thread(target=send_message, args=(app.app_context(),msg,))
    x.start()
    return 1