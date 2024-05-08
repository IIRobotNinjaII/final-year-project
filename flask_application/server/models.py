# models.py

from flask_login import UserMixin
from . import db
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from .enums import UserType, Department, Residence

def get_user_type(user_type_str):
    for user_type in UserType:
        if user_type.value == user_type_str:
            return user_type
    return None 

def get_user_email(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return user.email
    else:
        return None

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    policy = db.Column(db.String(1000))
    usertype = db.Column(db.Enum(UserType))
    department = db.Column(db.Enum(Department))
    residence = db.Column(db.Enum(Residence))

    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'name' : self.name,
            'policy': self.policy,
            'usertype': self.usertype.value if self.usertype else None,
            'department': self.department.value if self.department else None,
            'residence': self.residence.value if self.residence else None
        }

      
