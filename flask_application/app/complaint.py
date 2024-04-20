from flask import Flask, Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask_login import login_required, current_user
from .helpers import global_variables

complaint = Blueprint('complaint', __name__)

# Dummy data for demonstration purposes
complaints = [
    {"id": 1, "user_id": 2, "text": "This is a complaint from user 1"},
    {"id": 2, "user_id": 2, "text": "This is a complaint from user 2"},
    {"id": 3, "user_id": 2, "text": "Another complaint from user 1"}
]

@complaint.route('/complaint/view')
def view_complaints():
    url = 'http://example.com/api/data'
    response = requests.get(url)
    return render_template('view_complaints.html',complaints=response.json().get('complaints'))

@complaint.route('/complaint/file')
def file_complaint():
    return render_template('file_complaint.html')
