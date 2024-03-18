from flask_restful import Resource, Api
from flask import current_app as app
from flask import request 
from res.models.model import User
from res.generate import generate_otp,send_otp_sms
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_mail import Message
from res.utils import  mail
from flask_jwt_extended import (
    create_access_token, 
    jwt_required ,
    get_jwt_identity
)
import re
import uuid
import os 
from sqlalchemy import or_


# User Reistration API Endpoint
class registration(Resource):
    def post(self):
        data = request.get_json()
        
        firstname = data.get("firstName")
        lastname = data.get("lastName")
        email =  data.get("email")
        phone = data.get("phone")
        password = data.get("password")


        if User.query.filter_by(email = email).first():
            return{"IsError":"True","message":"Email already exists"}

        if not email:
            return{"IsError":"True" ,"message":"email is required"},400

        if phone and not re.match(r'^[0-9]{10}$', phone):
            return {"IsError": "True", "message": "Please enter a valid phone number"}, 400

        email_regex =  r'^[\w+\-.]+@[a-z\d\-]+(\.[a-z]+)*\.[a-z]+$'
        if not re.match(email_regex,email):
            return{"IsError":"True" , "mesaage":"please enter one upp valid email format"},400
            
        if not password:
            return {"IsError":"True" ,"message": "Password is required."}, 400
        
        

        pass_regex = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\w\s]).{8,}$'
        if not re.match(pass_regex, password):
            return {"IsError":"True" ,"message": "Please enter a valid password format."}, 400


        otp = generate_otp()
        
        user = User(firstname= firstname,
                lastname = lastname,
                email = email ,
                phone=phone,
                password=generate_password_hash(password, method='pbkdf2:sha256'),
                otp = otp ,
                otp_created_at= datetime.utcnow()  
                )
   
        user.save()

    
        msg=Message(subject='OTP',sender='phardik2130@gmail.com',recipients=[email])
        msg.body = f'Your Email Verification OTP: {otp}'
        mail.send(msg)

        send_otp_sms(phone, f'Your Phone Verification OTP: {otp}')
        return {"IsError":"False" ,"message":"otp send your email"},200
        

# OTP verify API End Point
class verify_otp(Resource):
    def post(self):
        # ------------- For email verification --------=

        # data = request.get_json()
        
        # email = data.get("email")
        # otp  = data.get("otp")

        # user = User.query.filter_by(email=email).first()
        # if not user:
        #     return {"IsError":"True" ,"message": "User not found."}, 404
        
        # if user.otp != otp:
        #     return {"IsError":"True" ,"message": "Invalid OTP."}, 400
        
        # # if user.otp == otp:
        # #     otp_expiration = user.otp_created_at + timedelta(minutes = 10)
        # #     if datetime.utcnow() > otp_expiration:
        # #         return {"message": "OTP has expired."},400

        # # OTP is valid, mark the user's email as verified
        # if user:
        #     user.is_email_verified = True
        #     user.otp = None
        # user.save()
        # return {"IsError":"False" ,"message": "Email verified successfull."}, 200
       

        # ------------ For Email or  Phone -----------

        data = request.get_json()
        
        email_or_phone = data.get("email_or_phone")
        otp = data.get("otp")

        user = User.query.filter(or_(User.email == email_or_phone, User.phone == email_or_phone)).first()
        if not user:
            return {"IsError": "True", "message": "User not found."}, 404
        
        if user.otp != otp:
            return {"IsError": "True", "message": "Invalid OTP."}, 400

        user.is_email_verified = True
        user.otp = None
        user.save()
        
        return {"IsError": "False", "message": "User verified successfully."}, 200


# Resend OTP API Endpoint
class resend_otp(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"IsError":"True" ,"message": "User not found."}, 404
        
        otp = generate_otp()

        user.otp = otp
        user.save()

        msg=Message(subject='OTP',sender='phardik2130@gmail.com',recipients=[email])
        msg.body = f'Your Email Verification New OTP: {otp}'
        mail.send(msg)
        return {"IsError":"False" ,"message":"otp send your email"},200


# User Login API Endpoint
class login(Resource):
    def post(self):
        email = request.json.get("email")
        password = request.json.get("password")

        user = User.query.filter_by(email = email).one_or_none()
            
        if not user.is_email_verified:
            return {"IsError":"True" ,"message":"Email not varified. Please verify your mail first"},400

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=email)
            response_data = {
                    'isError': False,
                    'message': 'User Login Successful',
                    'data': {
                        'accessToken': access_token
                    }
                }
            return response_data, 200
            
        else:
            return {"IsError":"True" ,"message":"login failed"}, 401
        
        
    @jwt_required()      #<------User Info --------->
    def get(self):
        email =  get_jwt_identity()
        user =  User.query.filter_by(email=email).first()


        if not user:
            return{'IsError':'True','message': 'User not found.'},404

        user_info= {
            'IsError':'False',
            'Message':'User Found',
            'data' :{
                'firstName': user.firstname,
                'lastName': user.lastname,
                'email': user.email,
                'phone':user.phone
            }
        }
        return user_info, 200   

# Send Link for Resetpassword
class PasswordResetLink(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")

        user = User.query.filter_by(email=email).first()
        if not user:
            return {'IsError':'True',"error": "User not found."}, 404
    
        reset_token = str(uuid.uuid4())

        user.reset_token = reset_token
        user.save()

        reset_link = f"http://127.0.0.1:5000/reset_password?token={reset_token}"

        msg = Message(
            subject="Password Reset",
            sender="phardik2130@gmail.com",
            recipients=[email],
            body=f"Click the following link to reset your password: {reset_link}",
        )
        mail.send(msg)

        return { 'IsError':'False',"message": "Password reset email sent successfully."}, 200


# User Reset Password API Endpoints
class PasswordReset(Resource):   
    def post(self):
        data = request.get_json()
        token = data.get("token")
        new_password = data.get("new_password")

        if not token:
            return {'IsError':'True',"error": "Token is required."}, 400
        if not new_password:
            return {'IsError':'True',"error": "New password is required."}, 400

       
        user = User.query.filter_by(reset_token=token).first()
        if not user:
            return {'IsError':'True',"error": "Invalid or expired token."}, 400

        # Reset user's password
        user.password = generate_password_hash(new_password)
        user.reset_token = None
        user.save()

        return { 'IsError':'False',"message": "Password reset successful."}, 200

# Update UserInfor API Endpoint
class UpdateUserInfo(Resource):
    @jwt_required()
    def put(self):
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        if not user:
            return {'IsError': 'True', 'message': 'User not found.'}, 404

        data = request.get_json()

        if 'firstName' in data:
            user.firstname = data['firstName']

        if 'lastName' in data:
            user.lastname = data['lastName']

        if 'phone' in data:
            user.phone = data['phone']

        if 'password' in data:
            new_password = data['password']
            pass_regex = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\w\s]).{8,}$'
            if not re.match(pass_regex, new_password):
                return {"IsError": "True", "message": "Please enter a valid password format."}, 400
            user.password = generate_password_hash(new_password, method='pbkdf2:sha256')

        user.save()
        return {'IsError': 'False', 'message': 'User profile updated successfully.'}, 200
