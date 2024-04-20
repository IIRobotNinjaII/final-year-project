from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from .models import User, UserType, get_user_type, Comment
from . import db
from .helpers import authorization

admin = Blueprint('admin', __name__)

# Admin route to approve users
@admin.route('/admin/approve/<int:user_id>',methods=['PUT'])
@authorization.role_required([UserType.ADMIN])
def approve_user(user_id):
    user = User.query.get_or_404(user_id)
    user.usertype = get_user_type(request.json['usertype'])
    user.policy = request.json['policy']
    db.session.commit()
    return jsonify({'message':f'User {user.id} has been approved.'})

# Admin route to view pending users
@admin.route('/admin/unapprovedofficers')
@authorization.role_required([UserType.ADMIN])
def unapproved_officers():
    unapproved_officers = User.query.filter_by(usertype=UserType.UNAPPROVED_OFFICER).all()
    unapproved_officers = [unapproved_officer.json() for unapproved_officer in unapproved_officers]
    return jsonify(unapproved_officers)

@admin.route('/admin/test', methods=['POST'])
def test():
    # db.session.query(Comment).delete()
    # db.session.commit()
    return "deleted",200