#!/usr/bin/env python3
"""
route to add and update data by brine attendant
"""
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from models import storage
from models.user import User
from models.salinity import Salinity
from .get_uuid_of_pan import get_id_of_pan
from datetime import date
from . import brine_attendant


@brine_attendant.route('/data_entry', methods=['GET', 'POST'])
@login_required
def data_entry():
    """
    Handles the data entry page for users.
    - On GET: Displays the data entry form for users to input relevant data.
    """
    if request.method == 'GET':
        return render_template('data_entry.html')
    

@brine_attendant.route('/add_record', methods=['POST'])
@login_required
def add_record():
    """
    Handles the submission of new salinity and brine level records.
    """
    #get data from form
    salinity_level =int(request.form['salinity'])
    brine_level=int(request.form["brine"])
    id_pan = get_id_of_pan(request.form["pan"])
    brine_attendant_id = current_user.id

    #add record
    salinity_reading = Salinity(
        salinity_level=salinity_level,
        brine_level=brine_level,
        pan_id=id_pan,
        brine_attendant_id=brine_attendant_id
    )

    # Save to the database
    salinity_reading.save()

    # Flash success message
    flash(f'Salinity data for {request.form["pan"]} submitted successfully!', 'success')

    # Redirect to the data entry page
    return redirect(url_for('brine_attendant.data_entry'))


@brine_attendant.route('/update_record', methods=['POST'])
@login_required
def update_record():
    """
    Update the latest existing salinity record for a specific pan,
    or create a new one if none exists.
    """
    # Get data from form
    salinity_level = int(request.form['salinity'])
    brine_level = int(request.form["brine"])
    id_pan = get_id_of_pan(request.form["pan"])
    brine_attendant_id = current_user.id

    if id_pan is None:
        flash('Invalid Pan selected!', 'error')
        return redirect(url_for('data_entry'))

    # Fetch today's salinity records and filter by Pan
    salinity_records_today = storage.get_all_by_date(Salinity, date.today())
    salinities_of_pan = storage.get_all_salinity_by_pan(salinity_records_today, 'id', id_pan)

    # Get latest entry
    latest_entry = storage.get_latest_record(salinities_of_pan)

    # Data to be updated
    data = {
        "salinity_level": salinity_level,
        "brine_level": brine_level,
        "pan_id": id_pan,
        "brine_attendant_id": brine_attendant_id
    }

    # Update existing record if found, otherwise create new record
    if latest_entry:
        for key, value in data.items():
            setattr(latest_entry, key, value)
        latest_entry.save()
        flash(f'Salinity data for {request.form["pan"]} updated successfully!', 'success')
    else:
        salinity_reading = Salinity(
            salinity_level=salinity_level,
            brine_level=brine_level,
            pan_id=id_pan,
            brine_attendant_id=brine_attendant_id
        )
        salinity_reading.save()
        flash(f'Salinity data for {request.form["pan"]} submitted successfully!', 'success')

    # Redirect to the data entry page
    return redirect(url_for('brine_attendant.data_entry'))
