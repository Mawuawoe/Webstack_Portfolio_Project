#!/usr/bin/python3
""" Authentication """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request
from flask_jwt_extended import create_access_token
from flasgger.utils import swag_from


@app_views.route('/auth/login', methods=['POST'], strict_slashes=False)
@swag_from('swagger_docs/auth/auth_login.yml')
def login():
    """
    Authenticate a user and return a JWT token
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        abort(400, description="Missing email or password")
    
    user = storage.get_first_by(User, email=email)
    if not user or not user.check_password(password):
        abort(401, description="Invalid credentials")

    # Create a JWT token
    access_token = create_access_token(
        identity=user.id,
        additional_claims={"role": user.role}
        )
    return jsonify({'msg': 'Login Successful',
                    'token': access_token}), 200
