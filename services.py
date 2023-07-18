from app import db,app
from models import User, Workout
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from sqlalchemy import func, text


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

def get_user_workout_progress(user_id, exercise_id):
    try:
        workout_data = (
            db.session.query(
                func.DATE_FORMAT(Workout.workout_datetime, '%Y-%m-%d').label('date'),
                func.avg(Workout.accuracy).label('average_accuracy'),
                func.avg(Workout.attempted_reps).label("attempted_reps")
            )
            .filter(
                Workout.user_id == user_id,
                Workout.exercise_id == exercise_id,
            )
            .group_by(text("DATE_FORMAT(workout_datetime, '%Y-%m-%d')"))
            .order_by(text("DATE_FORMAT(workout_datetime, '%Y-%m-%d')"))
            .all()
        )

        # Format the query result into a list of dictionaries
        formatted_data = [
            {'date': row[0], 'average_accuracy': row[1], "average_reps": row[2]}
            for row in workout_data
        ]

        return formatted_data
    except Exception as e:
        raise e

def parse_duration_str(duration_str):
    # Parse the duration string
    try:
        duration_obj = datetime.strptime(duration_str, "%H:%M:%S")

        # Calculate the total duration in seconds
        duration_mins = timedelta(hours=duration_obj.hour, minutes=duration_obj.minute, seconds=duration_obj.second).total_seconds()/60

        # Convert to integer duration
        duration_int = int(duration_mins)
    except Exception as e:
        raise e

    return duration_int

def get_user_stats(user_id):

    try:
        workouts = get_workout_history(user_id)

        total_workouts = len(workouts)
        total_duration = sum(parse_duration_str(workout.duration) for workout in workouts)
        avg_duration = total_duration / total_workouts if total_workouts else 0

        total_reps = sum(workout.attempted_reps for workout in workouts)
        avg_reps = total_reps / total_workouts if total_workouts else 0

        total_exercises = len(set(workout.exercise_id for workout in workouts))

        avg_accuracy = sum(workout.accuracy for workout in workouts) / total_workouts if total_workouts else 0

    except Exception as e:
        raise e

    return {
        "total_workouts": total_workouts,
        "total_duration": total_duration,
        "avg_duration": avg_duration,
        "total_reps": total_reps,
        "avg_reps": avg_reps,
        "total_exercises": total_exercises,
        "avg_accuracy": avg_accuracy,
    }