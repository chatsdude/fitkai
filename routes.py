from app import app
from flask import request, jsonify
from services import register_user

@app.route('/')
def home():
    return "Hello world from flask!!"

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    print(f"Data: {data}")
    register_user(username, email, password)
    return jsonify(message='User registered successfully')