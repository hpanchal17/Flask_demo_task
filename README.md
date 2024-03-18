1. create a virtual env
   Install requirements.txt

2. run the code
   python3 run.py

3. Run on :- http://127.0.0.1:5000

4. Open Postman

   1. For registeration API [POST]
      Url : http://127.0.0.1:5000/api/register
      Request :
      {
      "firstName":"your_first_name",
      "lastName": "your_first_name",
      "email": "test@mailinator.com",
      "phone":"your_phone_number",
      "password": "Abc@12345"
      }

   2. For User Otp Verify [POST]
      Url : http://127.0.0.1:5000/api/verify/otp
      Request:
      {
      "email_or_phone":"test1@mailinator.com",
      "otp" : 337014
      }

   3. For User Login [POST]
      Url: http://127.0.0.1:5000/api/user/login
      Request:
      {
      "email":"hp@mailinator.com",
      "password":"Abc@12345"
      }

   4. For User Information [GET]
      Url: http://127.0.0.1:5000/api/userinfo

   5. For UpdateUser [PUT]
      Url : http://127.0.0.1:5000/api/user/update
      Request:
      {
      "firstName":"demo",
      "lastName":"demo",
      "phone":"+919723491520",
      "password":"Demo@12345"
      }

   6. For Reset password Link [POST]
      Url: http://127.0.0.1:5000/api/user/update
      Request :
      {
      "email":"hardik@mailinator.com"
      }

   7. For Reset Password [POST]
      Url: http://127.0.0.1:5000/api/password
      Request:
      {
      "token":"a75178e3-dcfe-4919-a3fd-ebe464c49529",
      "new_password":"Test@12345"
      }
