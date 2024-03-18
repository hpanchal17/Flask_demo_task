from res.utils import db
from datetime import datetime ,timedelta
from res.generate import generate_uuid


class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.String(36), primary_key = True,default= generate_uuid)
    firstname = db.Column(db.String(50),nullable =False)
    lastname = db.Column(db.String(50),nullable = False)
    email = db.Column(db.String(50),unique=True,nullable=False)
    phone = db.Column(db.String(15),unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_email_verified = db.Column(db.Boolean)
    reset_token = db.Column(db.String(255))
    otp = db.Column(db.Integer)
    otp_created_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at =  db.Column(db.DateTime,default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
        
    def update(self):
        db.session.update(self)
        db.session.commit()
    



    
    