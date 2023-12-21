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


@app_views.route('/users', strict_slashes=False)
def all_users():
    all_users = storage.all(User).values()
    list_users = [user.to_dict() for user in all_users]
    return jsonify(list_users)


@app_views.route('/users/<user_id>', strict_slashes=False)
def specific_user(user_id):
    key = "User.{}".format(user_id)
    all_users = storage.all(User)
    if key in all_users:
        specific_user = all_users[key].to_dict()
        return jsonify(specific_user)
    else:
        abort(404)


@app_views.route(
        '/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_specific_user(user_id):
    key = "User.{}".format(user_id)
    all_users = storage.all(User)

    if key in all_users:
        user_to_delete = all_users[key]
        storage.delete(user_to_delete)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    if request.get_json():
        new_user_dict = request.get_json()
        if "email" in new_user_dict:
            if "password" in new_user_dict:
                new_user = User(**new_user_dict)
                new_user.save()
                response = new_user.to_dict()
                return jsonify(response), 201
            else:
                response = "Missing password"
                abort(400, response)
        else:
            response = "Missing email"
            abort(400, response)
    else:
        response = "Not a JSON"
        abort(400, response)


@app_views.route(
        '/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    key = "User.{}".format(user_id)
    all_users = storage.all(User)
    if key in all_users:
        specific_user = all_users[key]
    else:
        abort(404)
    if request.get_json():
        new_user_dict = request.get_json()
        ignore_keys = ["id", "created_at", "updated_at"]
        for key, value in new_user_dict.items():
            if key not in ignore_keys:
                setattr(specific_user, key, value)
        specific_user.save()
        specific_user = specific_user.to_dict()
        return (jsonify(specific_user))
    else:
        response = "Not a JSON"
        abort(400, response)
