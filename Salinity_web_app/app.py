#!/usr/bin/env python3
"""
Web Application serving both the frontend and api
"""
from flask import Flask, make_response, jsonify
from flask_login import LoginManager
import sys
sys.path.append("../")
from models import storage
from models.user import User
from webflask.blueprints.auth import auth_bp
from webflask.blueprints.dashboard import dashboard_bp
from webflask.blueprints.reports import report_bp
from webflask.blueprints.admin import admin_bp
from webflask.blueprints.brine_attendant import brine_attendant
from webflask.blueprints.landing_page import landing_page_bp
import os
from utils.seeded_data import seed_data
from api.v1.views import app_views
from flask_jwt_extended import JWTManager
from flasgger import Swagger


app = Flask(
    __name__,
    static_folder='webflask/static',
    template_folder='webflask/templates'
)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key') # secret key for session management
app.config['SESSION_COOKIE_SECURE'] = True  # or False for HTTP
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JWT_SECRET_KEY'] = 'my_jwt_secret_key'

# jwt login
jwt = JWTManager(app)


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
app.register_blueprint(app_views)


app.config['SWAGGER'] = {
    'title': 'Webstack_portfolio_project- Salinity Web_app Restful API',
    'uiversion': 3
}


Swagger(app)


@app.errorhandler(404)
def not_founf(error):
    """
    404 Error

    responses:
    404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the current database session after each request.
    """
    storage.close()


if __name__ == '__main__':
    with app.app_context():
        seed_data()  # Seed the database during app initialization
    app.run(host='0.0.0.0', port=5000, debug=True)
