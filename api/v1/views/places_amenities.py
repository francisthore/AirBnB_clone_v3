#!/usr/bin/python3
"""
Module to handle all endpoints for the
place amenities view
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from markupsafe import escape
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    """
    place = storage.get(Place, escape(place_id))
    if place is None:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    response = make_response(jsonify(amenities), 200)

    return response


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes an Amenity object to a Place by id
    """
    place = storage.get(Place, escape(place_id))
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, escape(amenity_id))
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    response = make_response(jsonify({}), 200)

    return response


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_place_amenity(place_id, amenity_id):
    """
    Creates a new Amenity object to a Place
    """
    place = storage.get(Place, escape(place_id))
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, escape(amenity_id))
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    response = make_response(jsonify(amenity.to_dict()), 201)

    return response
