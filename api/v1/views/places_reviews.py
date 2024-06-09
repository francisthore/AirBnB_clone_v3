#!/usr/bin/python3
"""
This module handles all default RESTful API actions for the Review object.
"""
from api.v1.views import app_views
from flask import  abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place.
    If the place_id is not linked to any Place object, raises a 404 error.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object.
    If the review_id is not linked to any Review object, raises a 404 error.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object.
    If the review_id is not linked to any Review object, raises a 404 error.
    Returns an empty dictionary with the status code 200.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review.
    If the place_id is not linked to any Place object, raises a 404 error.
    If HTTP body request is not valid JSON, raises 400 error with message
    If the dictionary doesn't contain user_id, raises 400 error with message
    If the user_id is not linked to any User object, raises a 404 error.
    If the dictionary doesn't contain key text, raises 400 error with message
    Returns the new Review with the status code 201.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    review = Review(**request.get_json())
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object.
    If the review_id is not linked to any Review object, raises a 404 error.
    If the HTTP request body is not valid JSON, raises a 400 error
    Update the Review object with all key-value pairs of the dictionary.
    Ignore keys: id, user_id, place_id, created_at and updated_at.
    Returns the Review object with the status code 200.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
