#!/usr/bin/env python3
"""
Web Application using Flask for Managing Salinity Data
"""


from flask import Flask
from flask_login import LoginManager
import sys
sys.path.append("../")
from models import storage
from models.user import User
from blueprints.auth import auth_bp
from blueprints.dashboard import dashboard_bp
from blueprints.reports import report_bp
from blueprints.admin import admin_bp
from blueprints.brine_attendant import brine_attendant
from blueprints.landing_page import landing_page_bp
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key') # secret key for session management
app.config['SESSION_COOKIE_SECURE'] = True  # or False for HTTP


# Flask-Login setup for session management
login_manager = LoginManager()
login_manager.init_app(app)
# Redirect users to login page if not authenticated
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    """Load user from the database by user ID (used by Flask-Login)."""
    return storage.get_by_id(User, user_id)


# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(report_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(brine_attendant)
app.register_blueprint(landing_page_bp)

@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the current database session after each request.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

