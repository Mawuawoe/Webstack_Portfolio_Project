#!/usr/bin/env python3
"""

"""

from flask import Blueprint

brine_attendant = Blueprint('brine_attendant', __name__, template_folder='../../templates')

from .routes import *
