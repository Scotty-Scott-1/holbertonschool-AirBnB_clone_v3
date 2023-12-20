#!/usr/bin/python3
"""made the app"""

from api.v1.views import app_views
from flask import Flask
import os
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception=None):
    """Call storage.close() here"""
    storage.close()


if __name__ == "__main__":
    """Retrieving host and port from environment variables"""
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    """Run the Flask server with specified configurations"""
    app.run(host=host, port=port, threaded=True)
