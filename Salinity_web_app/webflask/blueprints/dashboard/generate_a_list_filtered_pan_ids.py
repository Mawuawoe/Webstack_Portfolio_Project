#!/usr/bin/env python3
"""
a list of filtered pans, reserviors, pcr.
"""


def generate_filter_pan_ids(selected_filter):
    """
    Generate a list of pan IDs based on the selected filter.
    """
    # Initialize an empty list
    pan_ids = []

    # Depending on the filter, generate the appropriate pan_ids list
    if selected_filter == 'pan' or selected_filter == '':
        pan_ids.extend(f'Pan{i}' for i in range(1, 33))  # 1 to 32
    if selected_filter == 'reservoir' or selected_filter == '':
        pan_ids.extend(f'R{i}' for i in range(1, 6))  # 1 to 5
    if selected_filter == 'pcr' or selected_filter == '':
        pan_ids.extend(['PCRA', 'PCRB'])

    return pan_ids