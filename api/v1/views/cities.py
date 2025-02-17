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


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def all_cities(state_id):
    all_cities = storage.all(City).values()
    state = storage.get(State, state_id)

    if state:
        list_cities = [city.to_dict()
                       for city in all_cities if city.state_id == state_id]
        return jsonify(list_cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def specific_city(city_id):
    key = "City.{}".format(city_id)
    all_cities = storage.all(City)
    if key in all_cities:
        specific_city = all_cities[key].to_dict()
        return jsonify(specific_city)
    else:
        abort(404)


@app_views.route(
        '/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_specific_citie(city_id):
    key = "City.{}".format(city_id)
    all_cities = storage.all(City)

    if key in all_cities:
        city_to_delete = all_cities[key]
        storage.delete(city_to_delete)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET', 'POST'])
def create_city(state_id):

    if request.get_json():
        new_city_dict = request.get_json()
        state = storage.get(State, state_id)
        if state:
            if "name" in new_city_dict:
                new_city = City(**new_city_dict)
                new_city.state_id = state_id
                new_city.save()
                response = new_city.to_dict()
                return jsonify(response), 201
            else:
                response = "Missing name"
                abort(400, response)
        else:
            abort(404)
    else:
        response = "Not a JSON"
        abort(400, response)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    key = "City.{}".format(city_id)
    all_cities = storage.all(City)
    if key in all_cities:
        specific_city = all_cities[key]
    else:
        abort(404)
    if request.get_json():
        new_city_dict = request.get_json()
        ignore_keys = ["id", "created_at", "updated_at"]
        for key, value in new_city_dict.items():
            if key not in ignore_keys:
                setattr(specific_city, key, value)
        specific_city.save()
        specific_city = specific_city.to_dict()
        return (jsonify(specific_city))
    else:
        response = "Not a JSON"
        abort(400, response)
