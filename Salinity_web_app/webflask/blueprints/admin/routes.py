#!/usr/bin/env python3
"""
Module containing authentication feature
blueprint Auth
"""
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from models import storage
from models.user import User
from . import admin_bp


@admin_bp.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    """
    Handles the creation of an admin user in the application.
    
    - Redirects to login if an admin user already exists.
    - On GET: Displays the admin creation form if no admin exists.
    - On POST: Validates the form inputs and creates the first admin user.
    """
    # Check if an admin user already exists
    if request.method == 'GET':
        print("yes")
        existing_admin = storage.get_first_by(User, role="admin")
        print(existing_admin)
        if existing_admin:
            flash('Admin user already exists. Please log in.', 'info')
            print("Flash message sent: 'An admin user already exists. Please log in.'")
            return redirect(url_for('auth.login'))
        else:
            return render_template('create_admin.html')
    
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
            return redirect(url_for('create_admin'))
        
        # Create the admin user
        admin_user = User(
            email=email,
            first_name=firstname,
            last_name=lastname,
            username=username,
            contact_info=contact,
            role="admin"
        )
        admin_user.set_password(password)  # Hash the password before storing it
        admin_user.save()  # Save to the database
        
        flash('Admin user created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))


@admin_bp.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    """
    Handles the creation of a new user in the application, accessible only to the admin user.
    - On GET: Displays the user creation form.
    - On POST: Validates form inputs and creates a new user if the current user is an admin and the provided 
      email is not already registered.
    """
    if current_user.role != "admin":
        flash('Access denied. Only admin can create new users.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    if request.method == 'POST':
        role = request.form['role']
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
                           contact_info=contact,
                           role=role
                           )
        # Hash the password before storing it
        new_user.set_password(password)

        # Save to the database
        new_user.save()

        flash('User created successfully!', 'success')
        return redirect(url_for('auth.login'))
    
    flash('Only admin can create new users.', 'info')
    return render_template('register.html')

