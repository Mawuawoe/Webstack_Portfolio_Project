#!/usr/bin/env python3
"""

"""

from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__, template_folder='../../templates')

from .routes import *
