# models.py

from flask_login import UserMixin
from . import db
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship



class UserType(Enum):
    STUDENT = 'student'
    UNAPPROVED_OFFICER = 'unapproved_officer'
    OFFICER = 'officer'
    ADMIN = 'admin'
    # use this to  protect pages

    # status = db.Column(Enum(StatusEnum), default=StatusEnum.PENDING)
    # new_instance = YourModel(name='Example', status=StatusEnum.ACTIVE)
#     db.session.add(new_instance)
# db.session.commit()

def get_user_type(user_type_str):
    for user_type in UserType:
        if user_type.value == user_type_str:
            return user_type
    return None 
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    policy = db.Column(db.String(1000))
    usertype = db.Column(db.Enum(UserType))

    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'name' : self.name,
            'policy': self.policy,
            'usertype': self.usertype.value
        }

      
