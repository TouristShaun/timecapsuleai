from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from models import db, User  # Importing the User model from models.py
from config import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT

def init_app(app, db_config=None):
    if db_config is None:
        db_config = {
            'DATABASE_NAME': DATABASE_NAME,
            'DATABASE_USER': DATABASE_USER,
            'DATABASE_PASSWORD': DATABASE_PASSWORD,
            'DATABASE_HOST': DATABASE_HOST,
            'DATABASE_PORT': DATABASE_PORT,
        }

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_config["DATABASE_USER"]}:{db_config["DATABASE_PASSWORD"]}@{db_config["DATABASE_HOST"]}:{db_config["DATABASE_PORT"]}/{db_config["DATABASE_NAME"]}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)

def load_user(user_id):
    return User.query.get(int(user_id))

def register_user(username, email, password):
    user = User.query.filter_by(username=username).first()
    if user:
        return {"message": "Username already exists"}, 400

    new_user = User(
        username=username,
        email=email
    )
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return {"message": "Registered successfully"}, 201

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return {"message": "Invalid credentials"}, 401

    login_user(user)
    return {"message": "Logged in successfully"}, 200

def logout_user():
    logout_user()
    return {"message": "Logged out successfully"}, 200
