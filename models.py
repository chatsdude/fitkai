from datetime import datetime, timedelta
from app import db

#db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.DateTime)
    height = db.Column(db.Numeric(5, 2))
    weight = db.Column(db.Numeric(5, 2))
    goal = db.Column(db.Enum('lose_weight', 'gain', 'maintain'), nullable=False, default='maintain')
    created_on = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(minutes=120))
    updated_on = db.Column(db.DateTime)
    deleted_on = db.Column(db.DateTime)
    user = db.relationship('Workout', backref="user", lazy=True, uselist=False)

class GoalType(db.Model):
    __tablename__ = "GoalType"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_details.id'))
    goal = db.Column(db.Enum('lose_weight', 'gain', 'maintain'), nullable=False)

class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    birth_date = db.Column(db.DateTime)
    height = db.Column(db.Numeric(5, 2))
    weight = db.Column(db.Numeric(5, 2))
    goaltyperel = db.relationship('GoalType', backref='users')

    def __repr__(self):
        return f"UserDetails(id={self.user_id}, birth_date={self.birth_date}, goal_id={self.goal_id}, height={self.height})"

class Exercise(db.Model):
    __tablename__ = 'Exercise'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    created_on = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(minutes=120))
    updated_on = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(minutes=120))
    deleted_on = db.Column(db.DateTime)
    exercise = db.relationship('Workout', backref="exercise", lazy=True, uselist=False)


class Workout(db.Model):
    __tablename__ = 'Workout'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('Exercise.id'))
    duration = db.Column(db.String(20))
    total_reps = db.Column(db.Integer)
    attempted_reps = db.Column(db.Integer)
    accuracy = db.Column(db.Float)
    workout_datetime = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(minutes=120))
    created_on = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(minutes=120))
    updated_on = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(minutes=120))
    deleted_on = db.Column(db.DateTime)


class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    version_id = db.Column(db.String(50))
    algorithm_name = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, default=datetime.utcnow())
    deleted_on = db.Column(db.DateTime)

class ModelLogs(db.Model):
    sr_no = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    version_id = db.Column(db.String(50))
    request_id = db.Column(db.String(200))
    response_id = db.Column(db.String(200))
    request_body = db.Column(db.JSON)
    response_body = db.Column(db.JSON)
    prediction_prob = db.Column(db.Float)
    prediction_label = db.Column(db.Integer)
    model = db.relationship('Model', backref=db.backref('model_logs', lazy=True))

class ModelMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    training_date = db.Column(db.DateTime)
    performance_metrics = db.Column(db.String(200))
    training_data = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, default=datetime.utcnow())
    deleted_on = db.Column(db.DateTime)
    model = db.relationship('Model', backref=db.backref('model_metadata', lazy=True))
