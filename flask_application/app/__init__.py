# init.py

from flask import Flask, session
from flask_login import LoginManager 
from .helpers import crypto, global_variables

def create_app():
    app = Flask(__name__)
    
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for complaint filing and viewing parts of app
    from .complaint import complaint as complaint_blueprint
    app.register_blueprint(complaint_blueprint)

    return app

