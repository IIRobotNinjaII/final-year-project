from flask import  Blueprint,  request, jsonify,  session
from flask_login import login_required, current_user
from .helpers import global_variables,authorization
from .enums import UserType, ComplaintType, Department, Residence, AccountComplaintType, ResidentialComplaintType
from .models import get_user_email
import json
from charm.toolbox.msp import MSP
from charm.core.math.integer import serialize,deserialize
import requests
import uuid
from datetime import datetime

complaint = Blueprint('complaint', __name__)

@complaint.route('/complaint/file', methods=['POST'])
@login_required
@authorization.role_required([UserType.STUDENT])
def complaint_post():
    data = request.get_json()
    description = data.get('text')
    category = data.get('complaint type')
    user_id = current_user.id  

    # identity based encryption
    ibe_cipher_text = global_variables.ibe.encrypt(global_variables.ibe_master_public_key, str(user_id), description.encode())
    ibe_cipher_text['U'] = global_variables.ibe_group.serialize(ibe_cipher_text['U']).decode('iso-8859-1')
    ibe_cipher_text['V']=serialize(ibe_cipher_text['V']).decode('iso-8859-1')
    ibe_cipher_text['W']=serialize(ibe_cipher_text['W']).decode('iso-8859-1')

    # attribute based encryption
    # ComplaintType(request.json['complaint type']).name

    attributes = [] #determine attributes dynamically
    if category == 'residential':
        attributes.append(current_user.residence.name) 
        attributes.append(ResidentialComplaintType(data.get('residential complaint type')).name) 
    if category == 'account':
        attributes.append(AccountComplaintType(data.get('account complaint type')).name) 
    if category == 'academic':
        attributes.append(current_user.department.name)
    
    seperator = '#'
    cipher_text = global_variables.kpabe.encrypt(global_variables.master_public_key, description, attributes)
    for key in cipher_text['Ci']:
        cipher_text['Ci'][key]= global_variables.group.serialize(cipher_text['Ci'][key]).decode('iso-8859-1')
    
    # print(cipher_text)

    data = {
        'channelid': 'mychannel',
        'chaincodeid': 'complaint',
        'function': 'createAsset',
        'args': [
            str(uuid.uuid4()),
            seperator.join(attributes),
            json.dumps(cipher_text),
            json.dumps(ibe_cipher_text),
            str(user_id),
            datetime.now().isoformat()
        ]
    }

    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post("http://localhost:3000/invoke", data=data, headers=headers)
        if response.status_code == 200:
            return "Data sent to other API successfully", 200
        else:
            return "Failed to send data to other API", 500
    except Exception as e:
        return str(e), 500
    

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

def sortComplaints(response_dict):
    resolved_grouped_complaints = {}
    unresolved_grouped_complaints = {}
    for complaint in response_dict['complaints']:
        # print(complaint)
        if complaint['resolved']:
            group_dict = resolved_grouped_complaints
        else:
            group_dict = unresolved_grouped_complaints

        attributes = '|'.join(sorted(complaint['attributes']))
        if attributes not in group_dict:
            group_dict[attributes] = []
        group_dict[attributes].append(complaint)

    for group_dict in [resolved_grouped_complaints, unresolved_grouped_complaints]:
        for complaints in group_dict.values():
            complaints.sort(key=lambda x: x['created_at'], reverse=True)
    
    sorted_response={}
    sorted_response["resolved"]=resolved_grouped_complaints
    sorted_response["unresolved"]=unresolved_grouped_complaints

    return sorted_response

@complaint.route('/complaint/view', methods=['GET'])
@login_required
@authorization.role_required([UserType.ADMIN, UserType.OFFICER])
def complaint_get():
    
    url = "http://localhost:3000/query?channelid=mychannel&chaincodeid=complaint&function=GetAllAssets"
    headers = {
    'content-type': 'application/json'
    }
    payload={}
    response = requests.request("GET", url, headers=headers,data=payload)
    response_json = json.loads(response.text)
    
    # filtering complaints that user policy allows to decrypt
    user_complaints = []
    mspObj = MSP(global_variables.group)
    user_policy = mspObj.createPolicy(current_user.policy)
    for complaint in response_json:
        if mspObj.prune(policy=user_policy,attributes=complaint["attributes"]):
            user_complaints.append(complaint)

    policy_based_user_secret_key = session['secret_key']
    for key in policy_based_user_secret_key['Du']:
        policy_based_user_secret_key['Du'][key]=global_variables.group.deserialize(policy_based_user_secret_key['Du'][key].encode('iso-8859-1'))

    response = {"complaints": []}
    for user_complaint in user_complaints:
        user_complaint["attributes"] = user_complaint["attributes"].split('#')
        if user_complaint["description_user_copy"]:      
            user_complaint["description"] = deserialize_ciphertext(json.loads(user_complaint["description"]))
            user_complaint["description"] = global_variables.kpabe.decrypt(user_complaint["description"], policy_based_user_secret_key).decode('utf-8')
            
            payload1={}
            raw_comment = requests.request("GET", "http://localhost:3000/query?channelid=mychannel&chaincodeid=comment&function=QueryAssetsByComplaintID&args="+str(user_complaint["id"]), headers=headers,data=payload1) 
            user_complaint["comments"]=[]
            if raw_comment.text:
                comments = json.loads(raw_comment.text)
                for comment in comments:
                    comment["comment"] = deserialize_ciphertext(json.loads(comment["comment"]))
                    comment["comment"] = global_variables.kpabe.decrypt(comment["comment"], policy_based_user_secret_key).decode('utf-8')
                    user_complaint["comments"].append(comment)
            response["complaints"].append(user_complaint)

    return jsonify(sortComplaints(response))
    # return jsonify(response)

@complaint.route('/complaint/mycomplaints', methods=['GET'])
@login_required
@authorization.role_required([UserType.STUDENT])
def mycomplaint_get():
    user_id = current_user.id
    
    headers = {
    'content-type': 'application/json'
    }
    payload={}
    raw_user_complaints = requests.request("GET","http://localhost:3000/query?channelid=mychannel&chaincodeid=complaint&function=QueryAssetsByAuthorID&args="+str(current_user.id),headers=headers,data=payload)
    if not raw_user_complaints.text:
        return "Not Found",404
        
    user_complaints = json.loads(raw_user_complaints.text)
    master_secret_key = global_variables.ibe_master_secret_key
    master_public_key = global_variables.ibe_master_public_key
    private_key = global_variables.ibe.extract(master_secret_key, str(user_id))

    response = {"complaints": []}
    for user_complaint in user_complaints:
        complaint = {}
        user_complaint["attributes"] = user_complaint["attributes"].split('#')
        if user_complaint["description_user_copy"]:
            user_complaint["description_user_copy"]= deserialize_ibe_ciphertext((user_complaint["description_user_copy"]))
            user_complaint["description_user_copy"] = global_variables.ibe.decrypt(master_public_key, private_key, user_complaint["description_user_copy"]).decode()
            complaint = user_complaint
            
            payload1={}
            raw_comment = requests.request("GET", "http://localhost:3000/query?channelid=mychannel&chaincodeid=comment&function=QueryAssetsByComplaintID&args="+str(user_complaint["id"]), headers=headers,data=payload1) 
            if raw_comment.text:
                comments = json.loads(raw_comment.text)
                
                complaint["comments"]=[]
                for comment in comments:
                    comment["comment_user_copy"] = deserialize_ibe_ciphertext(comment["comment_user_copy"])
                    comment["comment_user_copy"] = global_variables.ibe.decrypt(master_public_key, private_key, comment["comment_user_copy"]).decode()
                    complaint["comments"].append(comment)
            response["complaints"].append(complaint)
    # response["complaints"] = sorted(response["complaints"], key=lambda x: x['complaint']['created_at'], reverse=True)
    # print(response)
    return jsonify(sortComplaints(response))
    return jsonify(response)

@complaint.route('/complaint/<complaint_id>', methods=['PUT'])
@login_required
@authorization.role_required([UserType.ADMIN, UserType.OFFICER])
# also required to have appropriate policy
def update_complaint(complaint_id):

    # get complaint
    url = "http://localhost:3000/query?channelid=mychannel&chaincodeid=complaint&function=ReadAsset&args=" + str(complaint_id)
    headers = {
    'content-type': 'x-www-form-urlencoded'
    }
    payload={}
    response = requests.request("GET", url, headers=headers,data=payload)
    if "does not exist" in response.text:
        return "Complaint not found",404
    complaint = json.loads(response.text)

    # check policy policy
    mspObj = MSP(global_variables.group)
    user_policy = mspObj.createPolicy(current_user.policy)
    print(mspObj.prune(policy=user_policy,attributes=complaint["attributes"]))
    if not mspObj.prune(policy=user_policy,attributes=complaint["attributes"]):
        return "Unauthorized", 401
        
    user_id = current_user.id
    complainant_id = complaint["author_id"]
    
    comment = request.get_json().get('comment')
    
    # identity based encryption
    ibe_cipher_text = global_variables.ibe.encrypt(global_variables.ibe_master_public_key, str(complainant_id), comment.encode())
    ibe_cipher_text['U'] = global_variables.ibe_group.serialize(ibe_cipher_text['U']).decode('iso-8859-1')
    ibe_cipher_text['V']=serialize(ibe_cipher_text['V']).decode('iso-8859-1')
    ibe_cipher_text['W']=serialize(ibe_cipher_text['W']).decode('iso-8859-1')

    # attribute based encryption
    cipher_text = global_variables.kpabe.encrypt(global_variables.master_public_key, comment, complaint["attributes"].split('#'))
    for key in cipher_text['Ci']:
        cipher_text['Ci'][key]= global_variables.group.serialize(cipher_text['Ci'][key]).decode('iso-8859-1')

    data = {
        'channelid': 'mychannel',
        'chaincodeid': 'comment',
        'function': 'createAsset',
        'args': [
            str(uuid.uuid4()),
            json.dumps(cipher_text),
            json.dumps(ibe_cipher_text),
            str(complaint_id),
            str(user_id),
            datetime.now().isoformat()
        ]
    }

    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post("http://localhost:3000/invoke", data=data, headers=headers)
        if response.status_code == 200:
            return "Data sent to other API successfully", 200
        else:
            return "Failed to send data to other API", 500
    except Exception as e:
        return str(e), 500
    
@complaint.route('/resolve-complaint/<complaint_id>', methods=['PUT'])
@login_required
@authorization.role_required([UserType.ADMIN, UserType.OFFICER])
def resolve_complaint(complaint_id):
    # get complaint
    url = f"http://localhost:3000/query?channelid=mychannel&chaincodeid=complaint&function=ReadAsset&args={complaint_id}"
    payload = {}
    headers = {
    'content-type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    complaint = json.loads(response.text)

    # check policy policy
    mspObj = MSP(global_variables.group)
    user_policy = mspObj.createPolicy(current_user.policy)
    print(mspObj.prune(policy=user_policy,attributes=complaint["attributes"]))
    if not mspObj.prune(policy=user_policy,attributes=complaint["attributes"]):
        return "Unauthorized", 401

    url = "http://localhost:3000/invoke"

    payload = '=&channelid=mychannel&chaincodeid=complaint&function=UpdateAsset&args='+ str(complaint_id) + "&args=" + str(current_user.id)
    headers = {
    'content-type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if not "Transaction ID " in response.text:
        return "Complaint not found",404
    else: 
        return "Complaint Resolved",200
    
