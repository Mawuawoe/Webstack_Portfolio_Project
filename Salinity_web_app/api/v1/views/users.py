#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flask_jwt_extended import jwt_required
from api.v1.utils.auth import role_required, get_current_user
from flasgger.utils import swag_from


@app_views.route('/initialize_first_admin', methods=['POST'], strict_slashes=False)
@swag_from('swagger_docs/user/initialize_admin.yml')
def initialize_admin():
    """
    Create the first admin user. This route is accessible only if no admin exists.
    """
    # Check if any admin user exists
    admin_exists = any(user.role == "admin" for user in storage.all(User).values())

    if admin_exists:
        abort(403, description="Admin already initialized. Route is disabled.")

    data = request.get_json()
    required_fields = ['email', 'password', 'first_name', 'last_name', 'username', 'contact_info']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    admin_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        username=data['username'],
        email=data['email'],
        contact_info=data['contact_info'],
        role="admin"
    )
    admin_user.set_password(data['password'])
    admin_user.save()

    return make_response(jsonify(admin_user.to_dict()), 201)


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@jwt_required()
@role_required(['admin'])
@swag_from('swagger_docs/user/all_users.yml')
def get_users():
    """
    Retrieves the list of all user objects
    (Admin-only operation)
    """
    # Fetch all users from storage
    all_users = storage.all(User).values()

    # Convert to a list of dictionaries
    list_users = [user.to_dict() for user in all_users]

    # Return the list of users
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
@role_required(["admin", "brine_attendant"])
@swag_from('swagger_docs/user/get_user.yml')
def get_user(user_id):
    """
    Retrieve a user
    """
    # Authenticate
    current_user = get_current_user()

    # Fetch the requested user
    user = storage.get_by_id(User, user_id)
    if not user:
        abort(404, description="User not found")

    # Authorization: Admins can get any user; others can get only themselves
    if current_user.role != 'admin' and current_user.id != user_id:
        abort(403, description="You do not have permission to view this user's information.")

    return jsonify(user.to_dict())



@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
@role_required(["admin", "brine_attendant"])
@swag_from('swagger_docs/user/delete_user.yml')
def delete_user(user_id):
    """
    Delete a user
    """
    # Authenticate
    current_user = get_current_user()

    # Fetch the user to delete
    user = storage.get_by_id(User, user_id)
    if not user:
        abort(404, description="User not found")

    # Authorization: Admins can delete any user; others can delete only themselves
    if current_user.role != 'admin' and current_user.id != user_id:
        abort(403, description="You do not have permission to perform this action.")

    # Delete the user
    storage.delete(user)
    storage.save()

    return make_response(jsonify({"message": "User deleted successfully"}), 200)

 
@app_views.route('/users', methods=['POST'], strict_slashes=False)
@jwt_required()
@role_required(["admin"])
@swag_from('swagger_docs/user/post_user.yml')
def post_user():
    """
    Create a new user (Admin-only operation).
    """
    # Parse the JSON payload
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    # Validate required fields
    required_fields = ["email", "password", "first_name", "last_name", "username", "contact_info", "role"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        abort(400, description=f"Missing fields: {', '.join(missing_fields)}")

    # Create and save the user instance
    try:
        instance = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            email=data['email'],
            contact_info=data['contact_info'],
            role=data['role']
        )
        instance.set_password(data['password'])
        instance.save()
    except Exception as e:
        # Handle duplicate or invalid data errors
        abort(400, description=str(e))

    # Return the created user
    return make_response(jsonify(instance.to_dict()), 201)



@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
@role_required(["admin", "brine_attendant"])
@swag_from('swagger_docs/user/put_user.yml')
def put_user(user_id):
    """
    Updates a user
    """
    # authenticate
    # Fetch the current user
    current_user = get_current_user()

    # Authorization: Admins can update any user, others can update only themselves
    if current_user.role != 'admin' and current_user.id != user_id:
        abort(403, description="You do not have permission to perform this action.")
    
    # update user
    user = storage.get_by_id(User, user_id)

    if not user:
        abort(404)
    
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            if key == 'password':  # Handle password updates explicitly
                user.set_password(value)  # Hash and set the password
            else:
                setattr(user, key, value)

    storage.save()
    return make_response(jsonify({"message": "User updated successfully"}), 200)
