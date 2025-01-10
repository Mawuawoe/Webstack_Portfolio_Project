#!/usr/bin/env python3
"""

"""

from flask import Blueprint

landing_page_bp = Blueprint('landing_page', __name__, template_folder='../../templates')

from .routes import *
