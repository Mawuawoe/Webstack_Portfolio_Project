#!/usr/bin/env python3
"""
Module/blueprint containing landing page route
index.html
"""
from flask import render_template
from . import landing_page_bp
from models import storage
from models.user import User


@landing_page_bp.route('/')
def index():
    """
    Home page of the app.
    
    - Redirects 'Get Started' to create admin if no admin exists.
    - Otherwise, redirects to the login page.
    """
    admin_exists = storage.get_first_by(User, role="admin") is not None
    return render_template('landing_page.html', admin_exists=admin_exists)
