#!/usr/bin/env python3
"""
report route
"""
from flask import Blueprint, render_template, request, redirect, url_for, Response, flash
from flask_login import login_required
from models import storage
from models.user import User
from models.salinity import Salinity
from models.pan import Pan
from datetime import date, datetime 
from .generate_a_list_filtered_pan_ids import generate_filter_pan_ids
from datetime import date, datetime
import pandas as pd
from io import StringIO
from . import report_bp


@report_bp.route('/report_page', methods=['GET', 'POST'])
@login_required
def report_page():
    """
    Renders the report page, allowing users to filter salinity records by date and type.
    
    - On GET: Displays an empty form for selecting a date and filter type.
    - On POST: Filters salinity records based on the selected date and filter type, 
      and renders the results in the template.
    """
    selected_date = request.args.get('date')
    selected_filter = request.args.get('filterType')
    if request.method == 'POST':
        selected_date = request.form.get('date', date.today().isoformat())
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
        selected_filter = request.form.get('filterType', '')

        pan_ids = generate_filter_pan_ids(selected_filter)

        #fetch all salinity records from today
        salinity_records_by_date = storage.get_all_by_date(Salinity, date_obj)
        
        # Dictionary to store records for each pan
        salinity_records = {}

        for pan_id in pan_ids:
            # Filter records by pan/reservoir/PCR
            salinities_for_pan_id = storage.get_all_salinity_by_pan(salinity_records_by_date, 'pan_id', pan_id)

            if salinities_for_pan_id:
                salinity_records[pan_id] = salinities_for_pan_id
            else:
                salinity_records[pan_id] = [{
                    "salinity_level": "NA",
                    "brine_level": "NA"
                }]
        return render_template('report_page.html',
                               salinity_records=salinity_records,
                               selected_date=selected_date,
                               selected_filter=selected_filter)
    return render_template('report_page.html',
                           salinity_records={},
                           selected_date=selected_date,
                           selected_filter=selected_filter)


@report_bp.route('/handle_selection', methods=['POST'])
@login_required
def handle_selection():
    """
     Handles user selection actions for updating or deleting salinity records.
    """
    action = request.form.get('action')
    selected_pan_ids = request.form.getlist('selected_pan_ids')
    selected_date = request.form.get('selected_date')
    selected_filter = request.form.get('selected_filter')

    if action == 'update' and selected_pan_ids:
        # only one record is allowed for update at a time
        return redirect(url_for('update', pan_id=selected_pan_ids[0]))
    elif action == 'delete' and selected_pan_ids:
        for pan_id in selected_pan_ids:
            record = storage.get_by_id(Salinity, pan_id)
            if record:
                print(record)
                storage.delete(record)
    return redirect(url_for('report.report_page', date=selected_date, filterType=selected_filter ))


@report_bp.route('/update/<pan_id>', methods=['GET', 'POST'])
@login_required
def update(pan_id):
    """
    Updates the salinity and brine level of a specific pan record.
    """
    record = storage.get_by_id(Salinity, pan_id)
    if request.method == "GET":
        print(record)
        return render_template('update.html', record=record)
    
    if request.method == 'POST':
        print(record)
        # Handle the form submission to update the record
        new_salinity = int(request.form['salinity'])
        setattr(record, "salinity_level", new_salinity)
        new_brine = int(request.form["brine"])
        setattr(record, 'brine_level', new_brine)
            
        #save changes
        record.save()

        flash(f'Salinity data updated successfully!', 'success')
        return redirect(url_for('update', pan_id=record.id))
    

@report_bp.route('/download_csv', methods=['POST'])
@login_required
def download_csv():
    """
    Generates and downloads a CSV file of salinity records filtered by date and pan type
    """

    # Get the selected date and filter from the form
    selected_date = request.form.get('selected_date')
    selected_filter = request.form.get('selected_filter')

    # Check if a date was selected
    if not selected_date:
        return redirect(url_for('report.report_page'))  
    
    # retrieve by date
    try:
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        return redirect(url_for('report.report_page')) 
    
    salinity_records_by_date = storage.get_all_by_date(Salinity, date_obj)

    # Create a list to hold all records
    records = []

    pan_ids = generate_filter_pan_ids(selected_filter)

    # Populate the records list with data
    for pan_id in pan_ids:
        salinities_for_pan_id = storage.get_all_salinity_by_pan(salinity_records_by_date, 'pan_id', pan_id)

        if salinities_for_pan_id:
            for record in salinities_for_pan_id:
                records.append({
                    'Pan ID': pan_id,
                    'Date': record.updated_at,
                    'Salinity Level': record.salinity_level,
                    'Brine Level': record.brine_level
                })
        else:
                records.append({
                    'Pan ID': pan_id,
                    'Date': "NA",
                    'Salinity Level': "NA",
                    'Brine Level': "NA"
                })

    # Create a DataFrame from the records
    df = pd.DataFrame(records)

    # Create a StringIO buffer
    output = StringIO()

    # Use the to_csv method to write to the response
    df.to_csv(output, index=False)

    # Get the CSV content from the buffer
    csv_content = output.getvalue()

    # Close the StringIO buffer
    output.close()

    # Create a CSV response
    response = Response(csv_content, content_type='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=salinity_records.csv'

    return response



