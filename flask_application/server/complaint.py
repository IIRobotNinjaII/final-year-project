from flask import Flask, Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask_login import login_required, current_user
from .helpers import global_variables
import copy
from . import db
from .models import Complaint
import json
from charm.toolbox.msp import MSP
from charm.core.math.integer import integer,serialize,deserialize

complaint = Blueprint('complaint', __name__)

# # Dummy data for demonstration purposes
# complaints = [
#     {"id": 1, "user_id": 1, "text": "This is a complaint from user 1"},
#     {"id": 2, "user_id": 1, "text": "This is a complaint from user 2"},
#     {"id": 3, "user_id": 1, "text": "Another complaint from user 1"}
# ]

#  is_admin = db.Column(db.Boolean, default=False) # add to user model
# # Authentication decorator to restrict access to admin-only routes
# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'user_id' not in session or not is_admin(session['user_id']):
#             flash('You do not have permission to access this page.', 'danger')
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function

@complaint.route('/complaint/file', methods=['POST'])
@login_required
def complaint_post():
    data = request.get_json()
    description = data.get('text')
    category = data.get('category')
    user_id = current_user.id  # Get user ID based on username

    ibe_cipher_text = global_variables.ibe.encrypt(global_variables.ibe_master_public_key, str(user_id), description.encode())
    ibe_cipher_text['U'] = global_variables.ibe_group.serialize(ibe_cipher_text['U']).decode('iso-8859-1')
    ibe_cipher_text['V']=serialize(ibe_cipher_text['V']).decode('iso-8859-1')
    ibe_cipher_text['W']=serialize(ibe_cipher_text['W']).decode('iso-8859-1')

    attributes = [global_variables.category_attribute[category] ] #determine attributes dynamically
    seperator = '#'
    cipher_text = global_variables.kpabe.encrypt(global_variables.master_public_key, description, attributes)
    for key in cipher_text['Ci']:
        cipher_text['Ci'][key]= global_variables.group.serialize(cipher_text['Ci'][key]).decode('iso-8859-1')
    # complaint = {"id": len(complaints) + 1, "user_id": user_id, "text": cipher_text}
    # complaints.append(complaint)
    complaint = Complaint(description=json.dumps(cipher_text),category=category, user_id=user_id, attributes = seperator.join(attributes),description_user_copy = json.dumps(ibe_cipher_text))
    
    db.session.add(complaint)
    db.session.commit()
    # print("##",complaints,"##")

    # user_id = current_user.id
    # user_complaints = Complaint.query.filter_by(user_id=user_id).all()
    # master_secret_key = global_variables.ibe_master_secret_key
    # master_public_key = global_variables.ibe_master_public_key
    # private_key = global_variables.ibe.extract(master_secret_key, str(user_id))

    # i=4
    # print(user_complaints[i].description_user_copy)
    # user_complaints[i].description_user_copy = deserialize_ibe_ciphertext(user_complaints[i].description_user_copy)
    # print(user_complaints[i].description_user_copy)
    # user_complaints[i].description_user_copy = global_variables.ibe.decrypt(master_public_key, private_key, user_complaints[i].description_user_copy)
    # print(user_complaints[i].description_user_copy)

    return "complaint registered", 200
    # return redirect(url_for('complaint.view_complaints'))

def deserialize_ciphertext(ciphertext):
    for key in ciphertext['Ci']:
        ciphertext['Ci'][key]= global_variables.group.deserialize(ciphertext['Ci'][key].encode('iso-8859-1'))
    return ciphertext

def deserialize_ibe_ciphertext(ciphertext):
    ciphertext =  json.loads(ciphertext)
    ciphertext['U'] = global_variables.ibe_group.deserialize(ciphertext['U'].encode('iso-8859-1'))
    ciphertext['V']=deserialize(ciphertext['V'].encode('iso-8859-1'))
    ciphertext['W']=deserialize(ciphertext['W'].encode('iso-8859-1'))
    return ciphertext
        
@complaint.route('/complaint/view', methods=['GET'])
@login_required
def complaint_get():
    # user_id = current_user.id
    all_complaints = Complaint.query.all()
    user_complaints = []

    mspObj = MSP(global_variables.group)
    user_policy = mspObj.createPolicy(current_user.policy)
    for complaint in all_complaints:
        print(complaint.attributes)
        if mspObj.prune(policy=user_policy,attributes=complaint.attributes):
            user_complaints.append(complaint)

    policy_based_user_secret_key = session['secret_key']
    # print(policy_based_user_secret_key)
    for key in policy_based_user_secret_key['Du']:
        # print(type(policy_based_user_secret_key['Du'][key]))
        policy_based_user_secret_key['Du'][key]=global_variables.group.deserialize(policy_based_user_secret_key['Du'][key].encode('iso-8859-1'))
        # print(type(policy_based_user_secret_key['Du'][key]))

    for i in range(len(user_complaints)):
        user_complaints[i].description = deserialize_ciphertext(json.loads(user_complaints[i].description))
        user_complaints[i].description = global_variables.kpabe.decrypt(user_complaints[i].description, policy_based_user_secret_key).decode('utf-8')

        if user_complaints[i].comment:
            user_complaints[i].comment = deserialize_ciphertext(json.loads(user_complaints[i].comment))
            user_complaints[i].comment = global_variables.kpabe.decrypt(user_complaints[i].comment, policy_based_user_secret_key).decode('utf-8')
    user_complaints_json = [user_complaint.json() for user_complaint in user_complaints]
    return jsonify(user_complaints_json)

@complaint.route('/complaint/mycomplaints', methods=['GET'])
@login_required
def mycomplaint_get():
    user_id = current_user.id
    user_complaints = Complaint.query.filter_by(user_id=user_id).all()
    master_secret_key = global_variables.ibe_master_secret_key
    master_public_key = global_variables.ibe_master_public_key
    private_key = global_variables.ibe.extract(master_secret_key, str(user_id))
    for i in range(len(user_complaints)):
        print(i)
        if user_complaints[i].description_user_copy:
            user_complaints[i].description_user_copy = deserialize_ibe_ciphertext(user_complaints[i].description_user_copy)
            user_complaints[i].description_user_copy = global_variables.ibe.decrypt(master_public_key, private_key, user_complaints[i].description_user_copy)
            if user_complaints[i].description_user_copy:
                user_complaints[i].description_user_copy=user_complaints[i].description_user_copy.decode() #dont need this if claened database
            if user_complaints[i].comment_user_copy:
                user_complaints[i].comment_user_copy = deserialize_ibe_ciphertext(user_complaints[i].comment_user_copy)
                user_complaints[i].comment_user_copy = global_variables.ibe.decrypt(master_public_key, private_key, user_complaints[i].comment_user_copy).decode()
    user_complaints_json = [user_complaint.json() for user_complaint in user_complaints]
    return jsonify(user_complaints_json)

@complaint.route('/complaint/<int:complaint_id>', methods=['PUT'])
@login_required
# also required to have appropriate policy
def update_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    user_id = complaint.user_id
    comment = request.get_json().get('comment')
    
    ibe_cipher_text = global_variables.ibe.encrypt(global_variables.ibe_master_public_key, str(user_id), comment.encode())
    ibe_cipher_text['U'] = global_variables.ibe_group.serialize(ibe_cipher_text['U']).decode('iso-8859-1')
    ibe_cipher_text['V']=serialize(ibe_cipher_text['V']).decode('iso-8859-1')
    ibe_cipher_text['W']=serialize(ibe_cipher_text['W']).decode('iso-8859-1')

    cipher_text = global_variables.kpabe.encrypt(global_variables.master_public_key, comment, complaint.attributes.split('#'))
    for key in cipher_text['Ci']:
        cipher_text['Ci'][key]= global_variables.group.serialize(cipher_text['Ci'][key]).decode('iso-8859-1')

    complaint.comment = json.dumps(cipher_text)
    complaint.comment_user_copy = json.dumps(ibe_cipher_text)

    db.session.commit()
    
    return jsonify(complaint.json()),200