#!/usr/bin/env python3
"""
Module containing route to the dashborad 
"""
from flask import render_template, request
from flask_login import current_user, login_required
from models import storage
from models.user import User
from models.salinity import Salinity
from models.pan import Pan
from datetime import date, datetime
from .generate_pan_name_list import generate_pan_ids 
from .generate_a_list_filtered_pan_ids import generate_filter_pan_ids
from . import dashboard_bp


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Displays the dashboard with salinity data based on filter and date.
    """
    admin_email = 'desmonddzakago@gmail.com' # Admin email for special permissions
    selected_filter = request.args.get('filter', '') # Filter type (pan, reservoir, PCR)
    selected_date = request.args.get('date', date.today().isoformat()) # Selected date
    date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()

    # Generate all pan IDs
    t_pan_ids = generate_pan_ids()

    # Get salinity data by date
    today_salinity = storage.get_all_by_date(Salinity, date_obj)

    # Organize salinity records
    today_records_dict = {}
    for t_pan_id in t_pan_ids:
        # Filter records by pan/reservoir/PCR
        today_salinity_by_pan = storage.get_all_salinity_by_pan(today_salinity, 'pan_id', t_pan_id)
        # Get the latest entry for the current pan/reservoir/PCR
        today_latest_entry = storage.get_latest_record(today_salinity_by_pan)
        if today_latest_entry:
            # Store the full instance if there's valid data
            today_records_dict[t_pan_id] = today_latest_entry
        else:
            # If no data is available, store "NA" for salinity_level and brine_level
            today_records_dict[t_pan_id] = {
                "salinity_level": "NA",
                "brine_level": "NA"
            }

    pan_ids = generate_filter_pan_ids(selected_filter)
    #fetch all salinity records from today
    salinity_records_today = storage.get_all_by_date(Salinity, date_obj)
    
    # Dictionary to store the latest records for each pan
    latest_records_dict = {}
    for pan_id in pan_ids:
        # Filter records by pan/reservoir/PCR
        salinities_for_current_pan = storage.get_all_salinity_by_pan(salinity_records_today, 'pan_id', pan_id)
        # Get the latest entry for the current pan/reservoir/PCR
        latest_entry = storage.get_latest_record(salinities_for_current_pan)
        if latest_entry:
            # Store the full instance if there's valid data
            latest_records_dict[pan_id] = latest_entry
        else:
            # If no data is available, store "NA" for salinity_level and brine_level
            latest_records_dict[pan_id] = {
                "salinity_level": "NA",
                "brine_level": "NA"
            }

    return render_template('dashboard.html',
                           is_admin=current_user.role == "admin",
                           latest_salinity_records=latest_records_dict,
                           selected_filter=selected_filter,
                           today_records=today_records_dict,
                           selected_date=selected_date
                           )
