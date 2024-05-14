from flask import request, Blueprint, jsonify
from .models import User, UserType, get_user_type
from . import db
from .helpers import authorization

admin = Blueprint('admin', __name__)

# Admin route to approve users
@admin.route('/admin/approve/<int:user_id>',methods=['PUT'])
# @authorization.role_required([UserType.ADMIN])
def approve_user(user_id):
    user = User.query.get_or_404(user_id)
    user.usertype = get_user_type(request.json['usertype'])
    user.policy = request.json['policy']
    db.session.commit()
    return jsonify({'message':f'User {user.id} has been approved.'})

# Admin route to view pending users
@admin.route('/admin/users',methods=['GET'])
# @authorization.role_required([UserType.ADMIN])
def officers():
    officers = User.query.filter_by().all()
    officers = [officer.json() for officer in officers]
    grouped_data = {}
    for officer in officers:
        usertype = officer['usertype']
        if usertype not in grouped_data:
            grouped_data[usertype] = []
        grouped_data[usertype].append(officer)
        
    return jsonify(grouped_data)

@admin.route('/admin/test', methods=['POST'])
def test():
    # db.session.query(Comment).delete()
    # db.session.commit()
    return "deleted",200