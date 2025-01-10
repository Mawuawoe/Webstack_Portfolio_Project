#!/usr/bin/env python3
"""
Module containing authentication feature
blueprint Auth
"""
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, UserMixin, login_required
from models import storage
from models.user import User
from . import auth_bp


# Define a UserMixin class to bridge with SQLAlchemy user model
"""class AuthUser(UserMixin):
    #Wrapper for the User class to be compatible with Flask-Login.
    def __init__(self, user):
        self.id = str(user.id) # Flask-Login requires user IDs as strings
        self.username = user.username
        self.email = user.email"""


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login route to authenticate users. Displays login form on GET and 
    handles authentication on POST.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print(f"Email: {email}, Password: {password}")  # Debugging line

        # Fetch the user from the database
        try:
            user = storage.get_first_by(User, email=email)
        except Exception as e:
            flash('An error occurred while processing your request.', 'danger')
            return render_template('login.html')
        # Check if user exists and if the password is correct
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Invalid credentials.', 'danger')
            return render_template('login.html')  # Render with error message

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """
    Logs the current user out of the application.
    """
    logout_user()  # This function logs the user out
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))  # Redirect to the login page
