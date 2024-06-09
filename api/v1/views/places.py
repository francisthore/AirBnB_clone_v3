#!/usr/bin/python3
"""
Places view module to handle all places
endpoints in our application
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from markupsafe import escape
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves a list of places"""
    city = storage.get(City, escape(city_id))
    if city is None:
        abort(404)
    response = jsonify([place.to_dict() for place in city.places])
    response.status_code = 200

    return response


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a place by id"""
    place = storage.get(Place, escape(place_id))
    if place is None:
        abort(404)
    response = jsonify(place.to_dict())
    response.status_code = 200

    return response


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place by id"""
    place = storage.get(Place, escape(place_id))
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    response = jsonify({})
    response.status_code = 200

    return response


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a place"""
    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')
    if 'user_id' not in data:
        abort(400, description='Missing user_id')
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    city = storage.get(City, escape(city_id))
    if city is None:
        abort(404)
    if 'name' not in data:
        abort(400, description='Missing name')
    data['city_id'] = city.id
    new_place = Place(**data)
    new_place.save()
    response = jsonify(new_place.to_dict())
    response.status_code = 200

    return response


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a place"""
    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')
    place = storage.get(Place, escape(place_id))
    if place is None:
        abort(404)
    for key, value in data.items():
        if key not in ['id', 'user_id',
                       'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    response = jsonify(place.to_dict())
    response.status_code = 200

    return response
