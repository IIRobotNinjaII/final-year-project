from functools import wraps
from flask import request, jsonify
from flask_login import current_user

def role_required(accepted_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is authenticated and has the specified role
            print(current_user.usertype, accepted_roles)
            if not current_user.is_authenticated or current_user.usertype not in accepted_roles:
                return jsonify({"message": "Unauthorized"}), 401
            return f(*args, **kwargs)
        return decorated_function
    return decorator