#!/usr/bin/python3
"""
Module for handling routes
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

# Define route for checking server status
@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    Returns server status
    :return: JSON response with server status
    """
    data = {
        "status": "OK"
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp

@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    Returns statistics for all objects
    :return: JSON response with object counts
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    # Create JSON response and set status code
    resp = jsonify(data)
    resp.status_code = 200

    return resp
