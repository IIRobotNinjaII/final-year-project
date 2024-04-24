from flask import  Blueprint,  request, jsonify, session
from flask_login import login_required, current_user
from .helpers import global_variables,authorization
from . import db
from .models import Complaint, Comment, UserType
import json
from charm.toolbox.msp import MSP
from charm.core.math.integer import serialize,deserialize

complaint = Blueprint('complaint', __name__)

@complaint.route('/complaint/file', methods=['POST'])
@login_required
@authorization.role_required([UserType.STUDENT.value])
def complaint_post():
    data = request.get_json()
    description = data.get('text')
    category = data.get('category')
    user_id = current_user.id  

    # identity based encryption
    ibe_cipher_text = global_variables.ibe.encrypt(global_variables.ibe_master_public_key, str(user_id), description.encode())
    ibe_cipher_text['U'] = global_variables.ibe_group.serialize(ibe_cipher_text['U']).decode('iso-8859-1')
    ibe_cipher_text['V']=serialize(ibe_cipher_text['V']).decode('iso-8859-1')
    ibe_cipher_text['W']=serialize(ibe_cipher_text['W']).decode('iso-8859-1')

    # attribute based encryption
    attributes = [global_variables.category_attribute[category] ] #determine attributes dynamically
    seperator = '#'
    cipher_text = global_variables.kpabe.encrypt(global_variables.master_public_key, description, attributes)
    for key in cipher_text['Ci']:
        cipher_text['Ci'][key]= global_variables.group.serialize(cipher_text['Ci'][key]).decode('iso-8859-1')
    
    complaint = Complaint(description=json.dumps(cipher_text), author_id=user_id, attributes = seperator.join(attributes),description_user_copy = json.dumps(ibe_cipher_text))
    db.session.add(complaint)
    db.session.commit()
    return "complaint registered", 200

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
@authorization.role_required([UserType.ADMIN.value, UserType.OFFICER.value])
def complaint_get():
    all_complaints = Complaint.query.all()

    # filtering complaints that user policy allows to decrypt
    user_complaints = []
    mspObj = MSP(global_variables.group)
    user_policy = mspObj.createPolicy(current_user.policy)
    for complaint in all_complaints:
        if mspObj.prune(policy=user_policy,attributes=complaint.attributes):
            user_complaints.append(complaint)

    policy_based_user_secret_key = session['secret_key']
    for key in policy_based_user_secret_key['Du']:
        policy_based_user_secret_key['Du'][key]=global_variables.group.deserialize(policy_based_user_secret_key['Du'][key].encode('iso-8859-1'))

    response = {"complaints": []}
    for user_complaint in user_complaints:
        complaint = {}
        if user_complaint.description_user_copy:
            user_complaint.description = deserialize_ciphertext(json.loads(user_complaint.description))
            user_complaint.description = global_variables.kpabe.decrypt(user_complaint.description, policy_based_user_secret_key).decode('utf-8')
            complaint['complaint'] = user_complaint.json()
            comments = Comment.query.filter_by(complaint_id=user_complaint.id)
            complaint["comments"]=[]
            for comment in comments:
                comment.comment = deserialize_ciphertext(json.loads(comment.comment))
                comment.comment = global_variables.kpabe.decrypt(comment.comment, policy_based_user_secret_key).decode('utf-8')
                complaint["comments"].append(comment.json())
            response["complaints"].append(complaint)
    return jsonify(response)

@complaint.route('/complaint/mycomplaints', methods=['GET'])
@login_required
@authorization.role_required([UserType.STUDENT.value])
def mycomplaint_get():
    user_id = current_user.id
    user_complaints = Complaint.query.filter_by(author_id=user_id).all()
    master_secret_key = global_variables.ibe_master_secret_key
    master_public_key = global_variables.ibe_master_public_key
    private_key = global_variables.ibe.extract(master_secret_key, str(user_id))

    response = {"complaints": []}
    for user_complaint in user_complaints:
        complaint = {}
        if user_complaint.description_user_copy:
            user_complaint.description_user_copy= deserialize_ibe_ciphertext(user_complaint.description_user_copy)
            user_complaint.description_user_copy = global_variables.ibe.decrypt(master_public_key, private_key, user_complaint.description_user_copy).decode()
            complaint['complaint'] = user_complaint.json()
            comments = Comment.query.filter_by(complaint_id=user_complaint.id)
            complaint["comments"]=[]
            for comment in comments:
                comment.comment_user_copy = deserialize_ibe_ciphertext(comment.comment_user_copy)
                comment.comment_user_copy = global_variables.ibe.decrypt(master_public_key, private_key, comment.comment_user_copy).decode()
                complaint["comments"].append(comment.json())
            response["complaints"].append(complaint)

    return jsonify(response)

@complaint.route('/complaint/<int:complaint_id>', methods=['PUT'])
@login_required
@authorization.role_required([UserType.ADMIN.value, UserType.OFFICER.value])
# also required to have appropriate policy
def update_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    user_id = current_user.id
    complainant_id = complaint.author_id
    comment = request.get_json().get('comment')
    
    # identity based encryption
    ibe_cipher_text = global_variables.ibe.encrypt(global_variables.ibe_master_public_key, str(complainant_id), comment.encode())
    ibe_cipher_text['U'] = global_variables.ibe_group.serialize(ibe_cipher_text['U']).decode('iso-8859-1')
    ibe_cipher_text['V']=serialize(ibe_cipher_text['V']).decode('iso-8859-1')
    ibe_cipher_text['W']=serialize(ibe_cipher_text['W']).decode('iso-8859-1')

    # attribute based encryption
    cipher_text = global_variables.kpabe.encrypt(global_variables.master_public_key, comment, complaint.attributes.split('#'))
    for key in cipher_text['Ci']:
        cipher_text['Ci'][key]= global_variables.group.serialize(cipher_text['Ci'][key]).decode('iso-8859-1')

    comment = Comment(comment=json.dumps(cipher_text), author_id=user_id,comment_user_copy = json.dumps(ibe_cipher_text), complaint_id=complaint_id)
    db.session.add(comment)
    db.session.commit()
    
    return "commented",200