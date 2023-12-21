#!/usr/bin/python3
"""handle default rest api actions """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/amenities', strict_slashes=False)
def all_amenities():
    all_amenities = storage.all(Amenity).values()
    list_amenities = [amenity.to_dict() for amenity in all_amenities]
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def specific_amenity(amenity_id):
    key = "amenity.{}".format(amenity_id)
    all_amenities = storage.all(Amenity)
    if key in all_amenities:
        specific_amenity = all_amenities[key].to_dict()
        return jsonify(specific_amenity)
    else:
        abort(404)


@app_views.route(
        '/amenities/<amenity_id>', strict_slashes=False, methods=['DELETE'])
def delete_specific_amenity(amenity_id):
    key = "amenity.{}".format(amenity_id)
    all_amenities = storage.all(Amenity)

    if key in all_amenities:
        amenity_to_delete = all_amenities[key]
        storage.delete(amenity_to_delete)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    if request.get_json():
        new_amenity_dict = request.get_json()
        if "name" in new_amenity_dict:
            new_amenity = Amenity(**new_amenity_dict)
            new_amenity.save()
            response = new_amenity.to_dict()
            return jsonify(response), 201
        else:
            response = "Missing name"
            abort(400, response)
    else:
        response = "Not a JSON"
        abort(400, response)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    key = "amenity.{}".format(amenity_id)
    all_amenities = storage.all(Amenity)
    if key in all_amenities:
        specific_amenity = all_amenities[key]
    else:
        abort(404)
    if request.get_json():
        new_amenity_dict = request.get_json()
        ignore_keys = ["id", "created_at", "updated_at"]
        for key, value in new_amenity_dict.items():
            if key not in ignore_keys:
                setattr(specific_amenity, key, value)
        specific_amenity.save()
        specific_amenity = specific_amenity.to_dict()
        return (jsonify(specific_amenity))
    else:
        response = "Not a JSON"
        abort(400, response)
