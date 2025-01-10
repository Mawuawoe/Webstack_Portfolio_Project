#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Saliities """
from models.salinity import Salinity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
import pandas as pd
import io
from flask_jwt_extended import jwt_required
from api.v1.utils.auth import role_required, get_current_user
from flasgger.utils import swag_from
from datetime import datetime


@app_views.route('/salinities', methods=['GET'], strict_slashes=False)
@jwt_required()
@role_required(['admin'])
@swag_from('swagger_docs/salinity/all_salinities_with_filters.yml')
def get_salinities():
    """
    Retrieve a list of salinities based on various filters such as date and pan type.
    Supports pagination through 'limit' and 'offset' query parameters.
    
    Admin only operation.

    Query Parameters:
    - date: Filters salinities by a specific date (or multiple dates).
    - pan_type: Filters salinities by pan type.
    - limit: Number of records per page (default is 10).
    - offset: The starting point for fetching records (default is 0).

    Returns:
    - A paginated list of salinities matching the provided filters.
    - Metadata about the pagination (total records, limit, offset, etc.).
    """
    
    # Initialize the filters dictionary for query parameters
    filters = {}
    # Validate 'date' filter
    if request.args.getlist('date'):
        dates = request.args.getlist('date')
        valid_dates = []
        for date in dates:
            try:
                # Check if the date is in 'YYYY-MM-DD' format
                datetime.strptime(date, "%Y-%m-%d")
                valid_dates.append(date)
            except ValueError:
                abort(400, description=f"Invalid date format: {date}. Use 'YYYY-MM-DD'.")
        filters['date'] = valid_dates

    # Validate 'pan_type' filter
    if request.args.get('pan_type'):
        pan_type = request.args.get('pan_type')
        valid_pan_types = ['Pan', 'PCR', 'Reservoir']  # Example valid types
        if pan_type not in valid_pan_types:
            abort(400, description=f"Invalid pan_type: {pan_type}. Expected one of {valid_pan_types}.")
        filters['pan_type'] = pan_type
    
    # Check if 'limit' and 'offset' are valid integers, otherwise abort
    try:
        limit = int(request.args.get('limit', 10))  # Default limit is 10
        offset = int(request.args.get('offset', 0))  # Default offset is 0
    except ValueError:
        abort(400, description="Invalid pagination parameters: 'limit' and 'offset' must be integers.")
    
    # Fetch the salinities with the given filters, limit, and offset
    salinities = storage.get_all_by(Salinity, filters, limit=limit, offset=offset)
    total_records = len(storage.get_all_by(Salinity, filters))  # Total records for pagination
    
    # If no records are found, return a 404 Not Found
    if not salinities:
        abort(404, description="No salinities found for the given filters.")
    
    # Convert the salinities objects to dictionaries
    list_salinities = [salinity.to_dict() for salinity in salinities]

    # Calculate the next and previous page URLs for pagination
    next_offset = offset + limit
    previous_offset = max(offset - limit, 0)

    # Prepare the metadata and response
    response = {
        "metadata": {
            "total_records": total_records,
            "limit": limit,
            "offset": offset,
            "returned_records": len(list_salinities),
            "next_page": f"/salinities?limit={limit}&offset={next_offset}" if next_offset < total_records else None,
            "previous_page": f"/salinities?limit={limit}&offset={previous_offset}" if offset > 0 else None
        },
        "salinities": list_salinities
    }

    return jsonify(response)


@app_views.route('/salinities/<dates>', methods=['GET'], strict_slashes=False)
@jwt_required()
@role_required(['admin'])
@swag_from('swagger_docs/salinity/get_salinities_by_dates.yml')
def get_salinities_date(dates):
    """
    Retrieve a list of salinities from a specified date or
    from a specified duration (list of dates).
    (Admin only operation)

    Path Parameter:
    - dates: A single date in 'YYYY-MM-DD' format or a comma-separated list of dates.
      Example: /salinities/2025-01-01 or /salinities/2025-01-01,2025-01-02
    """
    # Validate the dates
    date_list = dates.split(",")  # Split the input into individual dates
    valid_dates = []

    for date in date_list:
        try:
            # Check if each date is in 'YYYY-MM-DD' format
            datetime.strptime(date, "%Y-%m-%d")
            valid_dates.append(date)
        except ValueError:
            abort(400, description=f"Invalid date format: {date}. Use 'YYYY-MM-DD'.")

    if not valid_dates:
        abort(400, description="No valid dates provided.")

    # Fetch the salinities by date from storage
    try:
        salinity_by_date = storage.get_all_by_date(Salinity, valid_dates)
    except Exception as e:
        # Handle any errors that might occur while fetching salinities
        abort(400, description=f"Error fetching salinities: {str(e)}")

    # Convert salinities to a list of dictionaries
    list_salinities = [salinity.to_dict() for salinity in salinity_by_date]

    # Return the list of salinities as a JSON response
    return jsonify(list_salinities)



@app_views.route('/salinities/<salinity_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
@role_required(["admin"])
@swag_from('swagger_docs/salinity/get_salinity.yml')
def get_salinity(salinity_id):
    """
    Retrieve a specific salinity by ID.
    (Admin only operation)
    """
    # Fetch the salinity record by ID
    salinity = storage.get_by_id(Salinity, salinity_id)
    
    # If the salinity doesn't exist, return a 404 error
    if not salinity:
        abort(404, description="Salinity not found")
    
    # Return the salinity data as a JSON response
    return jsonify(salinity.to_dict())


@app_views.route('/salinities/<salinity_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
@role_required(['admin'])
@swag_from('swagger_docs/salinity/delete_salinity.yml')
def delete_salinity(salinity_id):
    """
    Deletes a salinity record.
    (Admin only operation)
    """
    # Fetch the salinity record by ID
    salinity = storage.get_by_id(Salinity, salinity_id)
    
    # If the salinity doesn't exist, return 404
    if not salinity:
        abort(404, description="Salinity not found")

    # Delete the salinity record from the storage (database)
    try:
        storage.delete(salinity)  # Assuming delete method removes the record
        storage.save()  # Commit the changes to the database
    except Exception as e:
        # If there's an issue with deletion, return an error
        abort(500, description=f"Error deleting salinity: {str(e)}")
    
    # Return a 200 OK response with an empty JSON object
    return make_response(jsonify({}), 200)


@app_views.route('/salinities', methods=['POST'], strict_slashes=False)
@jwt_required()
@role_required(['admin', 'brine_attendant'])
@swag_from('swagger_docs/salinity/post_salinity.yml')
def post_salinity():
    """
    Create a salinity record.
    (Anyone with the 'admin' or 'brine_attendant' role can post salinity data)
    """
    # Ensure the request contains JSON data
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    # Extract JSON data from the request
    data = request.get_json()
    
    # Ensure required fields are present in the data
    required_fields = ['salinity_level', 'brine_level', 'pan_id', 'brine_attendant_id']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")
    
    # Create a new Salinity instance using the provided data
    try:
        instance = Salinity(**data)
    except Exception as e:
        # If there are any issues creating the instance, return an error
        abort(400, description=f"Error creating salinity: {str(e)}")

    # Save the new salinity instance to the database
    instance.save()  # Assuming save method handles persistence

    # Return the created salinity object as a JSON response
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/salinities/<salinity_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
@role_required(["admin"])
@swag_from('swagger_docs/salinity/put_salinity.yml')
def put_salinity(salinity_id):
    """
    Updates a salinity record
    (Admin only operation)
    """
    # Fetch the salinity record from the database
    salinity = storage.get_by_id(Salinity, salinity_id)
    
    if not salinity:
        abort(404, description="Salinity not found")
    
    # Ensure the request contains JSON data
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    # Define which fields should not be updated (ignore them)
    ignore = ['id', 'created_at', 'updated_at']
    
    data = request.get_json()

    # Loop through the data and set attributes if they exist on the instance
    for key, value in data.items():
        if key not in ignore:
            # Ensure the attribute exists on the instance before setting it
            if hasattr(salinity, key):
                setattr(salinity, key, value)
            else:
                abort(400, description=f"Invalid attribute '{key}'")
    
    # Save the updated salinity instance
    salinity.save()

    # Return the updated salinity object as a JSON response
    return make_response(jsonify(salinity.to_dict()), 200)


@app_views.route('/salinities/export', methods=['GET'], strict_slashes=False)
@jwt_required()
@role_required(['admin'])
@swag_from('swagger_docs/salinity/export_salinities_to_csv.yml')
def export_salinities():
    """
    Exports salinity data as a CSV file using pandas.

    Query Parameters:
    - date: Filters salinities by specific date(s) in 'YYYY-MM-DD' format.
    - pan_type: Filters salinities by pan type (e.g., 'Pan', 'PCR', 'Reservoir').
    
    Returns:
    - A CSV file with the exported salinity data.
    """
    filters = {}

    # Validate 'date' filter
    if request.args.getlist('date'):
        dates = request.args.getlist('date')
        valid_dates = []
        for date in dates:
            try:
                # Check if the date is in 'YYYY-MM-DD' format
                datetime.strptime(date, "%Y-%m-%d")
                valid_dates.append(date)
            except ValueError:
                abort(400, description=f"Invalid date format: {date}. Use 'YYYY-MM-DD'.")
        filters['date'] = valid_dates

    # Validate 'pan_type' filter
    if request.args.get('pan_type'):
        pan_type = request.args.get('pan_type')
        valid_pan_types = ['Pan', 'PCR', 'Reservoir']  # Example valid types
        if pan_type not in valid_pan_types:
            abort(400, description=f"Invalid pan_type: {pan_type}. Expected one of {valid_pan_types}.")
        filters['pan_type'] = pan_type

    # Fetch salinities from storage based on filters
    salinities = storage.get_all_by(Salinity, filters)

    # Check if no data was found
    if not salinities:
        abort(404, description="No salinity data found for the specified filters.")

    # Convert salinity objects to a list of dictionaries
    salinity_dicts = [s.to_dict() for s in salinities]

    # Use pandas to create a DataFrame
    df = pd.DataFrame(salinity_dicts)

    # Create an in-memory buffer for the CSV
    output = io.BytesIO()

    # Write the DataFrame to the buffer as CSV
    df.to_csv(output, index=False)

    # Reset the buffer position to the beginning
    output.seek(0)

    # Prepare the response with the CSV content
    response = make_response(output.getvalue())
    
    # Set the response headers for file download
    response.headers["Content-Disposition"] = "attachment; filename=salinities.csv"
    response.headers["Content-Type"] = "text/csv"
    
    return response
