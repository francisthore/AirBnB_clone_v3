#!/usr/bin/python3
"""
Handles RESTFul API actions (CRUD) for the states
resource in our api project
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from markupsafe import escape
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects
    """
    states = [state.to_dict() for state in storage.all(State).values()]
    response = make_response(jsonify(states))

    return response


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a state object by id
    """
    state = storage.get(State, escape(state_id))
    if state is None:
        abort(404)
    response = make_response(jsonify(state.to_dict()))

    return response


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a state object by id
    """
    state = storage.get(State, escape(state_id))
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    response = make_response(jsonify({}))

    return response


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Create a new state object
    """
    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')
    if 'name' not in data:
        abort(400, description='Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Updates a state object"""
    state_id = escape(state_id)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        abort(400, description='Not a JSON')
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()))
