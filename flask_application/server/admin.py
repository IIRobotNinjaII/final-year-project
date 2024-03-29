from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from .models import User
from . import db

admin = Blueprint('admin', __name__)

# Admin route to approve users
@admin.route('/admin/approve/<int:user_id>',methods=['PUT'])
def approve_user(user_id):
    policy = request.json['policy']
    user = User.query.get_or_404(user_id)
    user.approved = True
    user.policy = policy
    db.session.commit()
    return jsonify({'message':f'User {user.id} has been approved.'})

# Admin route to view pending users
@admin.route('/admin/unapprovedofficers')
def unapproved_officers():
    unapproved_officers = User.query.filter_by(approved=False, usertype='unapproved_officer').all()
    unapproved_officers = [unapproved_officer.json() for unapproved_officer in unapproved_officers]
    return jsonify(unapproved_officers)

# if __name__ == '__main__':
#     db.create_all()
#     app.run(debug=True)
