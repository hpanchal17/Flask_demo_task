from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_jwt_extended import  (
    JWTManager,

)


db = SQLAlchemy()

mail = Mail()

jwt = JWTManager()

def init_db(app):
  db.init_app(app)

def create_all_tables():
    db.create_all()

