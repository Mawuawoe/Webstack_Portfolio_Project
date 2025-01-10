#!/usr/bin/env python3
"""
function to retrive pan.id by the pan_id submited
"""
from models import storage
from models.pan import Pan 

def get_id_of_pan(pan_id):
    """
    Retrieve the internal ID of a pan by its pan identifier
    """
    pan_objs = storage.all(Pan).values()
    for pan in pan_objs:
        if pan_id == pan.pan_id:
            return pan.id