#!/usr/bin/python3
"""handle default rest api actions """


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/states', strict_slashes=False)
def all_states():
    all_states = storage.all(State).values()
    list_states = [state.to_dict() for state in all_states]
    return jsonify(list_states)


@app_views.route('/states/<state_id>', strict_slashes=False)
def specific_state(state_id):
    key = "State.{}".format(state_id)
    all_states = storage.all(State)
    if key in all_states:
        specific_state = all_states[key].to_dict()
        return jsonify(specific_state)
    else:
        abort(404)


@app_views.route(
        '/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_specific_state(state_id):
    key = "State.{}".format(state_id)
    all_states = storage.all(State)

    if key in all_states:
        state_to_delete = all_states[key]
        storage.delete(state_to_delete)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    if request.get_json():
        new_state_dict = request.get_json()
        if "name" in new_state_dict:
            new_state = State(**new_state_dict)
            new_state.save()
            response = new_state.to_dict()
            return jsonify(response), 201
        else:
            response = "Missing name"
            abort(400, response)
    else:
        response = "Not a JSON"
        abort(400, response)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    key = "State.{}".format(state_id)
    all_states = storage.all(State)
    if key in all_states:
        specific_state = all_states[key]
    else:
        abort(404)
    if request.get_json():
        new_state_dict = request.get_json()
        ignore_keys = ["id", "created_at", "updated_at"]
        for key, value in new_state_dict.items():
            if key not in ignore_keys:
                setattr(specific_state, key, value)
        specific_state.save()
        specific_state = specific_state.to_dict()
        return (jsonify(specific_state))
    else:
        response = "Not a JSON"
        abort(400, response)
