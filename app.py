import logging
from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from backend.repositories.auth.user_repository import UserRepository
from backend.repositories.auth.session_repository import SessionRepository
from backend.services.auth.user_service import UserService

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

logging.basicConfig(level=logging.INFO)

@app.before_request
def before_request():
    g.db = db.session

@app.teardown_request
def teardown_request(exception=None):
    db.session.remove()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    user_repository = UserRepository(g.db)
    user_service = UserService(user_repository, None)  # SessionRepository not needed for registration
    user_id = user_service.register_user(email, password)

    return jsonify({"user_id": user_id}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user_repository = UserRepository(g.db)
    session_repository = SessionRepository(g.db)
    user_service = UserService(user_repository, session_repository)

    user = user_service.authenticate_user(email, password)
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401
    
    session = user_service.create_session(user)
    
    return jsonify({"token": session.token, "expires_at": session.expires_at.isoformat()}), 200

@app.route('/')
def index():
    return "Welcome to User Account Management"

if __name__ == '__main__':
    app.run(debug=True)