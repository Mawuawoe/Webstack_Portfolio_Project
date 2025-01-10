#!/usr/bin/env python3
"""

"""

from flask import Blueprint

report_bp = Blueprint('report', __name__, template_folder='../../templates/')

from .routes import *
