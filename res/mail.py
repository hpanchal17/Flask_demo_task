from flask_mail import Mail

def mail_db(app):
    mail = Mail(app)
