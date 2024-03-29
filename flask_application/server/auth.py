# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, Response, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
from .helpers import crypto, global_variables
import pickle
import dill
import base64
import json
import copy

auth = Blueprint('auth', __name__)

@auth.route('/login/user', methods=['POST'])
def login_users():
    email = request.json['email']
    password = request.json['password']
    # remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        return jsonify({'error': 'Invalid username or password'}), 401 # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    # login_user(user, remember=remember)
    policy = user.policy
    policy_based_user_secret_key = global_variables.kpabe.keygen(global_variables.master_public_key, global_variables.master_key, policy)
    # return jsonify(data), 200, {'Content-Type': 'application/json'}
    # return Response(redirect(url_for('main.profile',key="hello world"), code=200, Response=jsonify(data)),mimetype="application/json")
    
    # return jsonify({"master_public_key": global_variables.master_public_key,"master_key": global_variables.master_key, "secret_key": policy_based_user_secret_key}), 200
    # print("###",type(dill.dumps(global_variables.master_public_key)))
    # print(policy_based_user_secret_key)
    for key in policy_based_user_secret_key['Du']:
        # print(type(policy_based_user_secret_key['Du'][key]))
        policy_based_user_secret_key['Du'][key]=global_variables.group.serialize(policy_based_user_secret_key['Du'][key]).decode('iso-8859-1')
        # print(type(policy_based_user_secret_key['Du'][key]))

    # session['master_public_key']=master_public_key
    session['secret_key']=policy_based_user_secret_key

    login_user(user)
    
    # response = {"master_public_key": (global_variables.group.serialize(global_variables.master_public_key)).decode('iso-8859-1'), "secret_key": policy_based_user_secret_key}
    
    # for key in policy_based_user_secret_key['Du']:
    #     # print(type(policy_based_user_secret_key['Du'][key]))
    #     policy_based_user_secret_key['Du'][key]=global_variables.group.deserialize(policy_based_user_secret_key['Du'][key].encode('iso-8859-1'))
    #     # print(type(policy_based_user_secret_key['Du'][key]))

    # plaintext = global_variables.kpabe.decrypt(cipher_text, policy_based_user_secret_key)
    # print(plaintext)
    
    # mpk = global_variables.group.deserialize(response['master_public_key'].encode('iso-8859-1'))
    # sk = dict(response['secret_key'])

    return jsonify({"message":"Successful"}) , 200

@auth.route('/login/officer', methods=['POST'])
def login_officer():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password): 
        return jsonify({'error': 'Invalid username or password'}), 401 # if user doesn't exist or password is wrong, reload the page
    elif not user.approved:
        return jsonify({'message':'Your account is pending approval by the admin.'}), 202
    
    policy = user.policy
    policy_based_user_secret_key = global_variables.kpabe.keygen(global_variables.master_public_key, global_variables.master_key, policy)
    for key in policy_based_user_secret_key['Du']:
        policy_based_user_secret_key['Du'][key]=global_variables.group.serialize(policy_based_user_secret_key['Du'][key]).decode('iso-8859-1')

    session['secret_key']=policy_based_user_secret_key

    login_user(user)

    return jsonify({"message":"Successful"}) , 200

@auth.route('/signup/user', methods=['POST'])
def signup_user():
    if not request.is_json:
        return jsonify({'error':"Request does not contain JSON data"}), 400

    email = request.json['email']
    name = request.json['name']
    password = request.json['password']
    policy = 'STUDENT' #default policy for students request.json['policy']
    usertype = 'student'

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        return jsonify({'error': 'Email already exists'}), 409

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    # policy = '(ONE or THREE) and (THREE or TWO)' # replace with logic to dynamically decide policy

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), policy=policy, usertype=usertype)

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
    usertype = 'unapproved_officer'

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        return jsonify({'error': 'Email already exists'}), 409

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), policy='', usertype=usertype)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({ 'message': 'Your account has been created. Please wait for admin approval'}), 201