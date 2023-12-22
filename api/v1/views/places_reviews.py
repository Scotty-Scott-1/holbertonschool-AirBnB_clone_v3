#!/usr/bin/python3
"""handle default rest api actions """

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def all_reviews(place_id):
    all_reviews = storage.all(Review).values()
    place = storage.get(Place, place_id)

    if place:
        list_reviews = [review.to_dict()
                        for review in all_reviews
                        if review.place_id == place_id]
        return jsonify(list_reviews)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def specific_review(review_id):
    key = "Review.{}".format(review_id)
    all_reviews = storage.all(Review)
    if key in all_reviews:
        specific_review = all_reviews[key].to_dict()
        return jsonify(specific_review)
    else:
        abort(404)


@app_views.route(
        '/reviews/<review_id>', strict_slashes=False, methods=['DELETE'])
def delete_specific_review(review_id):
    key = "Review.{}".format(review_id)
    all_reviews = storage.all(Review)

    if key in all_reviews:
        review_to_delete = all_reviews[key]
        storage.delete(review_to_delete)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET', 'POST'])
def create_review(place_id):

    if request.get_json():
        new_review_dict = request.get_json()
        place = storage.get(Place, place_id)
        if place:
            if "text" in new_review_dict:
                if "user_id" in new_review_dict:
                    user = storage.get(User, new_review_dict["user_id"])
                    if user:
                        new_review = Review(**new_review_dict)
                        new_review.place_id = place_id
                        new_review.save()
                        response = new_review.to_dict()
                        return jsonify(response), 201
                    else:
                        abort(404)
                else:
                    response = "Missing user_id"
                    abort(400, response)
            else:
                response = "Missing text"
                abort(400, response)
        else:
            abort(404)
    else:
        response = "Not a JSON"
        abort(400, response)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    key = "Review.{}".format(review_id)
    all_reviews = storage.all(Review)
    if key in all_reviews:
        specific_review = all_reviews[key]
    else:
        abort(404)
    if request.get_json():
        new_review_dict = request.get_json()
        ignore_keys = ["id", "created_at", "updated_at", "user_id", "place_id"]
        for key, value in new_review_dict.items():
            if key not in ignore_keys:
                setattr(specific_review, key, value)
        specific_review.save()
        specific_review = specific_review.to_dict()
        return (jsonify(specific_review))
    else:
        response = "Not a JSON"
        abort(400, response)
