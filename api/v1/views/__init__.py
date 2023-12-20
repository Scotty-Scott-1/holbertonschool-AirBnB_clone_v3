#!/usr/bin/python3
""" init file"""

from flask import Blueprint
# Creating a Blueprint instance with URL prefix
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *