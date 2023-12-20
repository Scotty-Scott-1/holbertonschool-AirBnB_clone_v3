#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify

# Define a route /status on the app_views object
@app_views.route('/status')
def status():
    return jsonify({'status': 'OK'})
