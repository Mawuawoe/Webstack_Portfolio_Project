#!/usr/bin/env python3
"""
Module/blueprint containing landing page route
index.html
"""
from flask import render_template
from . import landing_page_bp


@landing_page_bp.route('/')
def index():
    """Render the login page."""
    return render_template('landing_page.html')
