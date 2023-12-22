#!/usr/bin/python3
"""made the app"""

from api.v1.views import app_views
from flask import Flask
from flask_cors import CORS
from flask import jsonify
import os
from models import storage

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception=None):
    """Call storage.close() here"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """Handler for 404 error"""
    response = {"error": "Not found"}
    return jsonify(response), 404


if __name__ == "__main__":
    """Retrieving host and port from environment variables"""
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    """Run the Flask server with specified configurations"""
    app.run(host=host, port=port, threaded=True)
