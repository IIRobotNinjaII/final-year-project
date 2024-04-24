from flask import Flask, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from .helpers import crypto, global_variables, ibe_crypto
from flask_migrate import Migrate


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True,render_as_batch=True)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from . import models

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return models.User.query.get(int(user_id))

    attributes = [ 'STUDENT', 'ACCOUNT', 'RESIDENTIAL', 'ACADEMIC', 'ADMIN' ]
    (global_variables.group, global_variables.kpabe, global_variables.master_public_key, global_variables.master_key) = crypto.initialize(attributes,50)
    (global_variables.ibe_group, global_variables.ibe, global_variables.ibe_master_public_key, global_variables.ibe_master_secret_key) = ibe_crypto.initialize(global_variables.ibe_master_public_key, global_variables.ibe_master_secret_key)
    
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for complaint filing and viewing parts of app
    from .complaint import complaint as complaint_blueprint
    app.register_blueprint(complaint_blueprint)
    
    # blueprint for admin routes 
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)



    return app



