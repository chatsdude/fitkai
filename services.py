from app import db,app
from models import User, Workout
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt


def register_user(username, email, password):
    hashed_password = generate_password_hash(password)
    user = User(name=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()

def authenticate_user(username, password):
    #Session = sessionmaker(bind=current_app.db.engine)
    #session = db.Session()

    user = db.session.query(User).filter_by(name=username).first()

    if user and user.password == password:
        return user
    return None

def generate_jwt_token(user):
    # Generate JWT token using a secret key
    jwt_secret = app.config['JWT_SECRET_KEY']
    #print(f"User: {user} - {user.id}")
    expiration_time = datetime.utcnow() + timedelta(minutes=10)
    expiration_time = expiration_time.timestamp()
    token_payload = {
        'user_id': user.id,
        'expiration_time': expiration_time,
    }
    token = jwt.encode(token_payload, jwt_secret, algorithm='HS256')
    return token

def update_user_preferences(id, birth_date, height, weight, goal):

    user = db.session.query(User).filter_by(id=id).first()

    if user and goal in ['gain', 'maintain', 'lose_weight']:
        user.birth_date = birth_date
        user.height = height
        user.weight = weight
        user.goal = goal
        db.session.commit()
        return True
    else:
        return False

def register_workout(user_id, duration,exercise_id,total_reps, attempted_reps, accuracy):
    try:
        workout = Workout(user_id=user_id,exercise_id=exercise_id, duration=duration, total_reps=total_reps, attempted_reps=attempted_reps, accuracy=accuracy)
        db.session.add(workout)
        db.session.commit()
        db.session.close()
    except Exception as e:
        raise e


def get_workout_history(user_id):
    try:
        workouts = db.session.query(Workout).filter_by(user_id=user_id).all()
        db.session.close()
    except Exception as e:
        raise e
    return workouts

