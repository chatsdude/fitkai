from app import db
from models import User
from werkzeug.security import generate_password_hash

def register_user(username, email, password):
    hashed_password = generate_password_hash(password)
    user = User(name=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
