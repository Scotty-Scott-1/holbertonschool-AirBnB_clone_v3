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


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def all_places(city_id):
    all_places = storage.all(Place).values()
    city = storage.get(City, city_id)

    if city:
        list_places = [place.to_dict()
                       for place in all_places if place.city_id == city_id]
        return jsonify(list_places)
    else:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False)
def specific_place(place_id):
    key = "Place.{}".format(place_id)
    all_places = storage.all(Place)
    if key in all_places:
        specific_place = all_places[key].to_dict()
        return jsonify(specific_place)
    else:
        abort(404)


@app_views.route(
        '/places/<place_id>', strict_slashes=False, methods=['DELETE'])
def delete_specific_place(place_id):
    key = "Place.{}".format(place_id)
    all_places = storage.all(Place)

    if key in all_places:
        place_to_delete = all_places[key]
        storage.delete(place_to_delete)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET', 'POST'])
def create_place(city_id):

    if request.get_json():
        new_place_dict = request.get_json()
        city = storage.get(City, city_id)
        if city:
            if "user_id" in new_place_dict:
                user = storage.get(User, new_place_dict["user_id"])
                if user:
                    new_place = Place(**new_place_dict)
                    new_place.city_id = city_id
                    new_place.save()
                    response = new_place.to_dict()
                    return jsonify(response), 201
                else:
                    abort(404)
            else:
                response = "Missing user_id"
                abort(400, response)
        else:
            abort(404)
    else:
        response = "Not a JSON"
        abort(400, response)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    key = "Place.{}".format(place_id)
    all_places = storage.all(Place)
    if key in all_places:
        specific_place = all_places[key]
    else:
        abort(404)
    if request.get_json():
        new_place_dict = request.get_json()
        ignore_keys = ["id", "created_at", "updated_at", "user_id", "city_id"]
        for key, value in new_place_dict.items():
            if key not in ignore_keys:
                setattr(specific_place, key, value)
        specific_place.save()
        specific_place = specific_place.to_dict()
        return (jsonify(specific_place))
    else:
        response = "Not a JSON"
        abort(400, response)
