from app import app, db
from flask import request, jsonify
from services import register_user, authenticate_user, generate_jwt_token, update_user_preferences, register_workout, get_workout_history
from functools import wraps
import jwt
from models import User
from datetime import datetime, timedelta
EXERCISE_MAPPING = {"Squats": 1, "Pushups":2, "Bicep Curls": 3}
REVERSED_EXERCISE_MAPPING = {1:"Squats", 2:"Pushups"}

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(
                token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()


            # checks if token is already blacklisted or not

            with open('/home/chaiasht/fitkai/blacklisted_tokens.txt', 'r') as file:
                blacklisted_tokens = file.read()
            blacklisted_tokens = blacklisted_tokens.split(',\n')
            is_token_valid = True if token not in blacklisted_tokens else False

            # checks if token is expired
            is_token_valid = is_token_valid and datetime.utcnow().timestamp() < data['expiration_time']

            if is_token_valid:
                return f(current_user, token, *args, **kwargs)
            else:
                return jsonify({'message': 'expired token, please log in to the system'})
        except Exception as e:
            return jsonify({
            "errorMsg": str(e)
        }), 500
    return decorator

@app.route('/')
def home():
    return f"Hello world!!"

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    print(f"Data: {data}")
    try:
        register_user(username, email, password)
    except:
        return jsonify(message='User registration failed')

    return jsonify(message='User registered successfully')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user = authenticate_user(username, password)
        if user:
            # Generate JWT token and return it to the client
            token = generate_jwt_token(user)
            return jsonify({'user_id': user.id, 'token': token})
        else:
            return jsonify(error='Invalid credentials'), 401
    except Exception as e:
        return jsonify({
            "errorMsg": str(e)
        }), 500

@app.route('/details', methods=['GET'])
@token_required
def details(user, token):

    try:
        data = jwt.decode(
                token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        #print(f"\n\n Name of User Received: {user.name}\n\n")
        results = db.session.query(User).filter_by(id=user.id).first()
        if results is not None:
            return jsonify({
                'name': results.name,
                'email': results.email,
                'birth_date': results.birth_date,
                'height': results.height,
                'weight': results.weight,
                'goal': results.goal
            })
        else:
            return jsonify(message=f'No User Found {-1}')
    except Exception as e:
        return jsonify({
            "errorMsg": str(e)
        }), 500

@app.route('/update/preferences', methods=['POST'])
@token_required
def update_preferences(user, token):

    try:
        data = request.json
        id = user.id
        birth_date = data.get('birth_date')
        height = data.get('height')
        weight = data.get('weight')
        goal = data.get('goal')
        update_result = update_user_preferences(
            id, birth_date, height, weight, goal)
        if update_result:
            return jsonify(message='User Details updated successfully')
        else:
            return jsonify(message='Update Failed!')
    except Exception as e:
        return jsonify({
            "errorMsg": str(e)
        }), 500

@app.route('/user/workout', methods=['POST'])
@token_required
def post_stats(user, token):
    try:
        data = request.json
        user_id = user.id
        exercise = data.get("exercise")
        exercise_id = EXERCISE_MAPPING.get(exercise)
        duration = data.get("duration")
        total_reps = data.get("total_reps")
        attempted_reps = data.get("attempted_reps")
        accuracy = (attempted_reps / total_reps) * 100
        register_workout(user_id, duration, exercise_id, total_reps, attempted_reps, accuracy)
    except Exception as e:
        return jsonify({
            "errorMsg": str(e)
        }), 500

    return jsonify(message="Workout registered successfully")

@app.route("/user/history", methods=["GET"])
@token_required
def get_history(user, token):
    try:
        user_id = user.id
        workouts = get_workout_history(user_id)
        formatted_data = [
                {'date': workout.workout_datetime,
                'exercise_name': REVERSED_EXERCISE_MAPPING.get(workout.exercise_id),
                "total_reps": workout.total_reps,
                "attempted_reps": workout.attempted_reps}
                for workout in reversed(workouts)
            ]
    except Exception as e:
        return jsonify({
            "errorMsg": str(e)
        }), 500
    return jsonify(workout_history = formatted_data)

@app.route('/logout', methods=['GET'])
@token_required
def logout(user, token):

    file_path = '/home/chaiasht/fitkai/blacklisted_tokens.txt'

    with open(file_path, 'a') as file:
        file.write(token + ',\n')

    return jsonify({
        'error': 'Logout successful',
        'token': token
    })

