# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, Response, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
import requests, json
from .models import User
from . import db
from .helpers import crypto, global_variables

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    # remember = True if request.form.get('remember') else False

    request_json_data = json.dumps({"email":email, "password":password})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(global_variables.login_url, data=request_json_data, headers=headers).json()

    print(response.json())
    # policy_based_user_secret_key = response['secret_key']
    # print(policy_based_user_secret_key)
    # for key in policy_based_user_secret_key['Du']:
    #     # print(type(policy_based_user_secret_key['Du'][key]))
    #     policy_based_user_secret_key['Du'][key]=global_variables.group.deserialize(policy_based_user_secret_key['Du'][key].encode('iso-8859-1'))
    #     # print(type(policy_based_user_secret_key['Du'][key]))

    # # plaintext = global_variables.kpabe.decrypt(cipher_text, policy_based_user_secret_key)
    # # print(plaintext)
    
    # master_public_key = global_variables.group.deserialize(response['master_public_key'].encode('iso-8859-1'))
    # # sk = dict(response['secret_key'])
    # text = "hello world"
    # attributes = [ 'ONE', 'TWO', 'THREE', 'FOUR' ]
    # cipher_text = global_variables.kpabe.encrypt(master_public_key, text, attributes)
    # print(cipher_text)
    # print(policy_based_user_secret_key)
    # plaintext = global_variables.kpabe.decrypt(cipher_text, policy_based_user_secret_key)
    # print(plaintext)

    return redirect(url_for('main.profile',key="hello world"))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    request_json_data = json.dumps({"email":email, "name":name, "password":password})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(global_variables.signup_url, data=request_json_data, headers=headers)

    if response.status_code == 201:
        return redirect(url_for('auth.login'))
    else:
        flash(response.json().get('error'))
        return render_template('signup.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))