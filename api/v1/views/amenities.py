#!/usr/bin/python3
"""
Amenities view module to handle all amenity api
endpoints
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from markupsafe import escape


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Retrieves a list of ammenities
    """
    amenities = storage.all(Amenity)
    response = jsonify([amenity.to_dict() for amenity in amenities.values()])
    response.status_code = 200

    return response


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_ammenity_by_id(amenity_id):
    """
    Retrieves an amenity by id
    """
    amenity = storage.get(Amenity, escape(amenity_id))
    if amenity is None:
        abort(404)
    response = jsonify(amenity.to_dict())
    response.status_code = 200

    return response


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes an amenity by id
    """
    amenity = storage.get(Amenity, escape(amenity_id))
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    response = jsonify({})
    response.status_code = 200

    return response


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates an amenity
    """
    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')
    if 'name' not in data:
        abort(400, description='Missing name')
    new_amenity = Amenity(**data)
    new_amenity.save()
    response = jsonify(new_amenity.to_dict())
    response.status_code = 201

    return response


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates an amenity
    """
    amenity = storage.get(Amenity, escape(amenity_id))
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    response = jsonify(amenity.to_dict())
    response.status_code = 200

    return response
