from os import environ
from flask import Flask ,request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from res.routes.route import (
    registration,
    verify_otp ,
    resend_otp ,
    login ,
    UpdateUserInfo,
    PasswordResetLink,
    PasswordReset
   
)
from res.models.model import User
from res.utils import init_db, create_all_tables, mail ,jwt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



app = Flask(__name__)

#Database URL ------
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/demo_task_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
app.config['JWT_SECRET_KEY'] = 'super-secret'


#Email Config--
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'phardik2130@gmail.com'
app.config['MAIL_PASSWORD'] = 'eqnekajrwibrlwtdu'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
       


api = Api(app)

init_db(app)

mail.init_app(app)
jwt.init_app(app)


api.add_resource(registration,'/api/register')
api.add_resource(verify_otp , '/api/verify/otp')
api.add_resource(resend_otp, '/api/verify/otp/resend')
api.add_resource(login , '/api/user/login', '/api/userinfo')
api.add_resource(PasswordResetLink,'/api/resetPassword')
api.add_resource(PasswordReset,'/api/password')
api.add_resource(UpdateUserInfo,'/api/user/update')


if __name__ == '__main__':
    with app.app_context():
        create_all_tables()
    app.run(debug=True, host="0.0.0.0", port= 5000)


