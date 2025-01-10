#!/usr/bin/env python3
"""
Module containing authentication feature
blueprint Auth
"""
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from models import storage
from models.user import User
import os
from . import admin_bp


@admin_bp.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    """
    Handles the creation of an admin user in the application.
    
    - On GET: Displays the admin creation form.
    - On POST: Validates the form inputs and creates an admin user if the environment is set to 'dev' 
      and the provided email is not already registered.
    """
    if request.method == 'POST':
        if os.getenv('FLASK_ENV') != 'dev':
            flash('Access denied.', 'danger')
            return redirect(url_for('auth.login'))

        admin_email = 'desmonddzakago@gmail.com'
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        contact = request.form['contact']
        password = request.form['password']

        # Check if the email already exists
        if storage.get_first_by(User, email=email):
            flash('Email already registered', 'danger')
            return redirect(url_for('create_admin'))
        
        # Create a admin user
        admin_user1 = User(email=email,
                           first_name=firstname,
                           last_name=lastname,
                           username=username,
                           contact_info=contact
                           )
        
        admin_user1.set_password(password)  # Hash the password before storing it

        # Save to the database
        admin_user1.save()

        flash('Admin user created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('create_admin.html')  # Render the form when GET


@admin_bp.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    """
    Handles the creation of a new user in the application, accessible only to the admin user.
    - On GET: Displays the user creation form.
    - On POST: Validates form inputs and creates a new user if the current user is an admin and the provided 
      email is not already registered.
    """
    admin_email = 'desmonddzakago@gmail.com'
    if current_user.email != admin_email:
        flash('Access denied. Only admin can create new users.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        contact = request.form['contact']
        password = request.form['password']

        # Check if the email already exists
        if storage.get_first_by(User, email=email):
            flash('Email already registered', 'danger')
            return redirect(url_for('admin.create_user'))
        
        # Creates a user
        new_user = User(email=email,
                           first_name=firstname,
                           last_name=lastname,
                           username=username,
                           contact_info=contact
                           )
        # Hash the password before storing it
        new_user.set_password(password)

        # Save to the database
        new_user.save()

        flash('User created successfully!', 'success')
        return redirect(url_for('auth.login'))
    
    flash('Only admin can create new users.', 'info')
    return render_template('register.html')

