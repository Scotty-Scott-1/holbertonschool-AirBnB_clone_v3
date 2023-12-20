#!/usr/bin/python3


from flask import Blueprint

# Creating a Blueprint instance with URL prefix
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Define your routes and functionalities for this Blueprint
# For example:
@app_views.route('/endpoint')
def my_endpoint():
    return 'This is my API endpoint'

# More routes and functionalities can be added here

# Register this Blueprint with your Flask app
app.register_blueprint(app_views)

# Wildcard import of everything in the package api.v1.views.index
from api.v1.views.index import *  # noqa: F401,F403
