#!/usr/bin/python3
"""
Module to handle user api endpoints in our
application
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from markupsafe import escape
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
def get_users():
    """
    get all users
    """
    users = storage.all(User)
    response = jsonify([user.to_dict() for user in users.values()])
    response.status_code = 200

    return response


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    find user using id
    """
    user = storage.get(User, escape(user_id))
    if user is None:
        abort(404)
    response = jsonify(user.to_dict())
    response.status_code = 200

    return response


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    delete a user using id
    """
    user = storage.get(User, escape(user_id))
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    response = jsonify({})
    response.status_code = 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    creates a new user
    """
    data = request.get_json()
    if data is None:
        abort(404)
    if 'email' not in data:
        abort(400, description='Missing email')
    if 'password' not in data:
        abort(400, description='Missing password')
    new_user = User(**data)
    storage.save(new_user)
    response = jsonify(new_user.to_dict())
    response.status_code = 201

    return response


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    delete a user
    """
    user = storage.get(User, escape(user_id))
    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['email', 'id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    response = jsonify(user.to_dict())
    response.status_code = 200

    return response
