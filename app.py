import logging
from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from backend.repositories.auth.user_repository import UserRepository
from backend.repositories.auth.session_repository import SessionRepository
from backend.repositories.auth.password_reset_repository import PasswordResetRepository
from backend.repositories.products.product_repository import ProductRepository
from backend.repositories.products.category_repository import CategoryRepository
from backend.services.auth.user_service import UserService
from backend.services.auth.password_reset_service import PasswordResetService
from backend.services.products.product_service import ProductService

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
    user_service = UserService(user_repository, None)
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

@app.route('/request-password-reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    user_repository = UserRepository(g.db)
    password_reset_repository = PasswordResetRepository(g.db)
    password_reset_service = PasswordResetService(password_reset_repository, user_repository)

    token = password_reset_service.request_password_reset(email)
    if not token:
        return jsonify({"error": "Password reset request failed"}), 400

    return jsonify({"message": "Password reset requested", "token": token}), 200

@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password')
    if not token or not new_password:
        return jsonify({"error": "Token and new password are required"}), 400

    user_repository = UserRepository(g.db)
    password_reset_repository = PasswordResetRepository(g.db)
    password_reset_service = PasswordResetService(password_reset_repository, user_repository)

    success = password_reset_service.reset_password(token, new_password)
    if not success:
        return jsonify({"error": "Password reset failed"}), 400

    return jsonify({"message": "Password reset successful"}), 200

@app.route('/update-profile', methods=['POST'])
def update_profile():
    data = request.get_json()
    user_id = data.get('user_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    preferences = data.get('preferences')

    if user_id is None:
        return jsonify({"error": "User ID is required"}), 400

    user_repository = UserRepository(g.db)
    user_service = UserService(user_repository, None)
    user_service.update_profile(user_id, first_name, last_name, preferences)

    return jsonify({"message": "Profile updated successfully"}), 200

@app.route('/add-product', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')
    category_id = data.get('category_id')

    if not name or price is None or not description:
        return jsonify({"error": "Name, price and description are required"}), 400

    product_repository = ProductRepository(g.db)
    category_repository = CategoryRepository(g.db)
    product_service = ProductService(product_repository, category_repository)

    try:
        product_id = product_service.add_product(name, price, description, category_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Product added successfully", "product_id": product_id}), 201

@app.route('/')
def index():
    return "Welcome to User Account Management"

if __name__ == '__main__':
    app.run(debug=True)