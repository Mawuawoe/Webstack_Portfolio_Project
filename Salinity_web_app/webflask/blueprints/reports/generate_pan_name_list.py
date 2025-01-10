#!/usr/bin/env python3
"""
a list of pans, reserviors, pcr.
"""

def generate_pan_ids():
    """
    Generate a list of pan IDs.
    """
    # Initialize an empty list
    pan_ids = []
    # Generate Pan IDs from Pan1 to Pan32
    pan_ids.extend(f'Pan{i}' for i in range(1, 33))  # 1 to 32
    # Generate Reservoir IDs from R1 to R5
    pan_ids.extend(f'R{i}' for i in range(1, 6))  # 1 to 5
    # Add PCR IDs
    pan_ids.extend(['PCRA', 'PCRB'])

    return pan_ids
