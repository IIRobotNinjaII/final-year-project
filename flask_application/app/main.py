# main.py

from flask import Blueprint, render_template, request, session
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile/<key>')
@login_required
def profile(key):
    if 'key' in session:
        # Get the key from the session
        key = session['key']
        # Render the profile page with the key
        return render_template('profile.html', name=current_user.name, key=key)
    else:
        # Redirect to the login page if user is not logged in
        return redirect(url_for('login'))