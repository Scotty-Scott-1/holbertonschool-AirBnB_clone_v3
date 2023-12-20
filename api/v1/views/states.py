#!/usr/bin/pyhton3
"""handle default rest api actions """

from api.v1.views import app_views
from flask import jsonify, abort
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

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
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
