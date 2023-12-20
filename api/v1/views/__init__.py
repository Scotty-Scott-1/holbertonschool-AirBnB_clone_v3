#!/usr/bin/python3
""" init file"""


from flask import Blueprint
from api.v1.views.index import *


# Creating a Blueprint instance with URL prefix
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Define routes and functionalities for this Blueprint
@app_views.route('/endpoint')
def my_endpoint():
    return 'This is my API endpoint'

# Register this Blueprint with your Flask app
app.register_blueprint(app_views)
