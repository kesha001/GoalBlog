# import threading
# from flask_mail import Message
# from app import mail
# from flask import current_app

# def send_message(app_context, msg):
#     app_context.push()
#     mail.send(msg)


# def send_error_mail(e, tb):
#     msg = Message(
#         subject=e.description,
#         sender=current_app.config['MAIL_USERNAME'],
#         recipients=["berdstudy@gmail.com"],
#         body=tb,
#     )
#     x = threading.Thread(target=send_message, args=(current_app.app_context(),msg,))
#     x.start()
#     return 1