# auth.py

from flask import Blueprint, request, jsonify,  session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from .models import User, UserType, Department, Residence
from . import db
from .helpers import  global_variables

# import json

auth = Blueprint('auth', __name__)

@auth.route('/login/user', methods=['POST'])
def login_users():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()

    # check if user is registered and password is correct
    if not user or not check_password_hash(user.password, password): 
        return jsonify({'error': 'Invalid username or password'}), 401

    # set secret key according to policy
    policy = user.policy
    policy_based_user_secret_key = global_variables.kpabe.keygen(global_variables.master_public_key, global_variables.master_key, policy)
    for key in policy_based_user_secret_key['Du']:
        policy_based_user_secret_key['Du'][key]=global_variables.group.serialize(policy_based_user_secret_key['Du'][key]).decode('iso-8859-1')
    session['secret_key']=policy_based_user_secret_key
    login_user(user)

    return jsonify({"message":"Successful"}) , 200
    # return jsonify(data), 200, {'Content-Type': 'application/json'}
    # return Response(redirect(url_for('main.profile',key="hello world"), code=200, Response=jsonify(data)),mimetype="application/json")

@auth.route('/login/officer', methods=['POST'])
def login_officer():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password): # if user doesn't exist or password is wrong
        return jsonify({'error': 'Invalid username or password'}), 401 
    elif user.usertype == UserType.UNAPPROVED_OFFICER: # if user is an unapproved officer
        return jsonify({'message':'Your account is pending approval by the admin.'}), 202
    
    policy = user.policy
    policy_based_user_secret_key = global_variables.kpabe.keygen(global_variables.master_public_key, global_variables.master_key, policy)
    for key in policy_based_user_secret_key['Du']:
        policy_based_user_secret_key['Du'][key]=global_variables.group.serialize(policy_based_user_secret_key['Du'][key]).decode('iso-8859-1')
    session['secret_key']=policy_based_user_secret_key
    login_user(user)

    return jsonify(user.json()) , 200

@auth.route('/signup/user', methods=['POST'])
def signup_user():
    if not request.is_json:
        return jsonify({'error':"Request does not contain JSON data"}), 400

    email = request.json['email']
    name = request.json['name']
    password = request.json['password']
    department = Department(request.json['department'])
    residence = Residence(request.json['residence'])
    usertype = UserType.STUDENT
    policy = f"({residence.value} or {department.value})"

    user = User.query.filter_by(email=email).first() 
    if user: # Email already exists in database
        return jsonify({'error': 'Email already exists'}), 409

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'),policy=policy, usertype=usertype, department=department, residence=residence)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({ 'message': 'User signed up successfully!'}), 201

@auth.route('/signup/officer', methods=['POST'])
def signup_officer():
    if not request.is_json:
        return jsonify({'error':"Request does not contain JSON data"}), 400

    email = request.json['email']
    name = request.json['name']
    password = request.json['password']
    policy = ''
    usertype = UserType.UNAPPROVED_OFFICER
    department = Department.NOTAPPLICABLE
    residence = Residence.NOTAPPLICABLE

    user = User.query.filter_by(email=email).first() 
    if user: # Email already exists in database
        return jsonify({'error': 'Email already exists'}), 409

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'),policy=policy, usertype=usertype, department=department, residence=residence)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({ 'message': 'Your account has been created. Please wait for admin approval'}), 201