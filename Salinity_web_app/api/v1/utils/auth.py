#!/usr/bin/python3
""" Authentication helper functions"""
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity
from functools import wraps
from flask import abort
from flask import g
from models import storage
from models.user import User

def role_required(required_roles):
    """
    Decorator to restrict access based on roles.

    :param required_roles: List of roles allowed to access the route
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()  # Ensure the JWT token is valid
            claims = get_jwt()  # Extract claims from the JWT token
            
            # Check if role exists and is authorized
            if "role" not in claims or claims["role"] not in required_roles:
                abort(403, description="You do not have permission to perform this action.")
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def get_current_user():
    """
    Fetch the current user based on the JWT identity, with caching.
    """
    if "current_user" not in g:  # Check if already cached
        current_user_id = get_jwt_identity()  # Extract user ID from JWT
        if not current_user_id:
            abort(401, description="Invalid token or no identity in token")
        user = storage.get_by_id(User, current_user_id)  # Fetch from DB
        if not user:
            abort(401, description="Unauthorized: User not found")
        g.current_user = user
    return g.current_user
