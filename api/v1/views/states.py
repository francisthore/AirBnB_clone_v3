#!/usr/bin/python3
"""
Handles RESTFul API actions (CRUD) for the states
resource in our api project
"""

from api.v1.views import app_views
from flask import jsonify, abort
from markupsafe import escape
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects
    """
    states = [state.to_dict() for state in storage.all("State").values()]
    response = jsonify(states)
    response.status_code = 200

    return response


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a state object by id
    """
    state = storage.get(State, escape(state_id))
    if state is None:
        abort(404)
    response = jsonify(state.to_dict())
    response.status_code = 200

    return response
