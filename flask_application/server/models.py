# models.py

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    policy = db.Column(db.String(1000))
    usertype = db.Column(db.String(100))
    approved = db.Column(db.Boolean, default=False)

    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'name' : self.name,
            'policy': self.policy,
            'usertype': self.usertype,
            'approved' : self.approved,
        }
        
class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20), default='Admin')
    attributes = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    comment = db.Column(db.Text, nullable=True) #later add as a comment list with associated user ids
    description_user_copy = db.Column(db.Text, nullable=True)
    comment_user_copy = db.Column(db.Text, nullable=True) #later add as a comment list with associated user ids

    # Define foreign key relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('complaints', lazy=True))

    def json(self):
        return {
            'id': self.id,
            'description': self.description,
            'comment' : self.comment,
            'user_id': self.user_id,
            'description_user_copy': self.description_user_copy,
            'comment_user_copy' : self.comment_user_copy,
        }


