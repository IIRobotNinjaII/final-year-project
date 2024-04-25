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

      
# class Complaint(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     attributes = db.Column(db.Text, nullable=False)
#     description = db.Column(db.Text)
#     description_user_copy = db.Column(db.Text)
#     created_at = db.Column(DateTime, default=datetime.utcnow)
#     resolved = db.Column(Boolean, default=False)  # New boolean field

#     # Foreign key reference to User
#     author_id = db.Column(Integer, ForeignKey('user.id'))
#     author = relationship("User")

#     def json(self):
#         return {
#             'id': self.id,
#             'description': self.description,
#             'description_user_copy': self.description_user_copy,
#             'created_at' : self.created_at,
#             'resolved' : self.resolved,
#             'author_id' : self.author_id,
#         }

# class Comment(db.Model):
#     id = db.Column(Integer, primary_key=True)
#     comment = db.Column(String)
#     comment_user_copy = db.Column(String)
#     created_at = db.Column(DateTime, default=datetime.utcnow)

#     # Foreign key reference to User, renamed to author_id
#     author_id = Column(Integer, ForeignKey('user.id'))
#     author = relationship("User")

#     # Foreign key reference to Complaint
#     complaint_id = Column(Integer, ForeignKey('complaint.id'))
#     complaint = relationship("Complaint")

#     def json(self):
#         return {
#             'id': self.id,
#             'comment' : self.comment,
#             'comment_user_copy' : self.comment_user_copy,
#             'created_at' : self.created_at,
#             'complaint_id' : self.complaint_id,
#             'author_id' : self.author_id,
#         }