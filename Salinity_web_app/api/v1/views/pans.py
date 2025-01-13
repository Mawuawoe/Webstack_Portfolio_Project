#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Pans """
from models.pan import Pan
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flask_jwt_extended import jwt_required
from api.v1.utils.auth import role_required
from flasgger.utils import swag_from


@app_views.route('/pans', methods=['GET'], strict_slashes=False)
@jwt_required()
@role_required(['admin'])
@swag_from('swagger_docs/pan/all_pans.yml')
def get_pans():
    """
    Retrieve the list of all pan objects (Admin only operation)
    """
    try:
        all_pans = storage.all(Pan).values()  # Get all pans
        if not all_pans:
            abort(404, description="No pans found")  # If no pans are found

        list_pans = [pan.to_dict() for pan in all_pans]  # List comprehension to convert pans to dict
    except Exception as e:
        abort(500, description=f"Error retrieving pans: {str(e)}")  # Handle database or storage errors

    return jsonify(list_pans)  # Return the list of pans as JSON


@app_views.route('/pans/<pan_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
@role_required(['admin'])
@swag_from('swagger_docs/pan/get_pan.yml')
def get_pan(pan_id):
    """
    Retrieve a pan (Admin only operation)
    """
    try:
        pan = storage.get_by_id(Pan, pan_id)
        if not pan:
            abort(404, description="Pan not found")  # More informative error message
    except Exception as e:
        abort(500, description=f"Error retrieving pan: {str(e)}")  # Handle database errors

    return jsonify(pan.to_dict())  # Return the pan's data as JSON


@app_views.route('/pans/<pan_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
@role_required(['admin'])
@swag_from('swagger_docs/pan/delete_pan.yml')
def delete_pan(pan_id):
    """
    Deletes a pan (Admin only operation)
    """
    pan = storage.get_by_id(Pan, pan_id)
    if not pan:
        abort(404, description="Pan not found")

    try:
        storage.delete(pan)  # Try to delete the pan
        storage.save()       # Save the changes to the database
    except Exception as e:
        abort(500, description=f"Error deleting pan: {str(e)}")  # Handle any errors during deletion

    return make_response(jsonify({"message": "Pan deleted successfully"}), 200)


@app_views.route('/pans', methods=['POST'], strict_slashes=False)
@jwt_required()
@role_required(['admin'])
@swag_from('swagger_docs/pan/post_pan.yml')
def post_pan():
    """
    Create a pan (Admin only operation)
    """
    data = request.get_json()  # Retrieve JSON data only once
    if not data:
        abort(400, description="Not JSON")
    
    # Check for missing required fields
    required_fields = ['location', 'pan_id', 'size', 'pan_type']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")
    
    # Additional validation: Ensure size is an integer
    if not isinstance(data['size'], int):
        abort(400, description="Size must be an integer")

    # Check for duplicate pan_id
    existing_pan = storage.get_by_id(Pan, data['pan_id'])
    if existing_pan:
        abort(400, description="Pan ID already exists")

    # Create the new pan instance
    instance = Pan(**data)
    
    try:
        instance.save()  # Save the new pan instance
    except Exception as e:
        abort(500, description=f"Error saving pan: {str(e)}")  # Handle database errors

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/pans/<pan_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
@role_required(['admin'])
@swag_from('swagger_docs/pan/put_pan.yml')
def put_pan(pan_id):
    """
    Updates a pan (Admin only operation).
    """
    pan = storage.get_by_id(Pan, pan_id)
    if not pan:
        abort(404, description="Pan not found")

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignore = ['id', 'created_at', 'updated_at']
    
    for key, value in data.items():
        if key not in ignore:
            if hasattr(pan, key): # Ensures the key is a valid attribute of the pan object
                setattr(pan, key, value)
            else:
                abort(400, description=f"Invalid attribute: {key}")

    try:
        storage.save() # Ensure save commits the changes correctly
    except Exception as e:
        abort(500, description=str(e))  # Handle potential database save errors

    return make_response(jsonify({"message": "Pan updated successfully"}), 200)

