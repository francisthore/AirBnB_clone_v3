#!/usr/bin/python3
"""
api that handles all default api action for cities
endpoints in our application
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State
from markupsafe import escape


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city_by_state(state_id):
    """
    get all cities related to a state
    """

    state = storage.get(State, escape(state_id))
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    response = jsonify(cities)
    response.status_code = 200

    return response


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def find_city(city_id):
    """
    retrieve a city by id
    """
    city_id = escape(city_id)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    response = jsonify(city.to_dict())
    response.status_code = 200

    return response


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    deletes a city by id:get city -> delete
    """
    city_id = escape(city_id)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    response = jsonify({})
    response.status_code = 200

    return response


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a new city
    """
    state_id = escape(state_id)
    info = request.get_json()
    if info is None:
        abort(404, description='Not a JSON')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if 'name' not in info:
        abort(400, description='Missing name')

    data = {"state_id": state_id, "name": info['name']}
    new_city = City(**data)
    new_city.save()
    response = jsonify(new_city.to_dict())
    response.status_code = 200


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    update city details, given id
    """
    city_id = escape(city_id)
    info = request.get_json()
    if info is None:
        abort(404, description='Not a JSON')
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for key, value in info.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    response = jsonify(city.to_dict())
    response.status_code = 200

    return response
