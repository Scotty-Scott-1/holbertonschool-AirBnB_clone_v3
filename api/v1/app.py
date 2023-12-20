#!/usr/bin/python3

from models import storage
from api.v1.views import app_views
from flask import Flask

app = Flask(__name__)

# Method to handle teardown_appcontext
@app.teardown_appcontext
def close_storage(exception=None):
    # Call storage.close() here
    storage.close()

# Your Flask routes and other functionalities go here

if __name__ == "__main__":
    # Retrieving host and port from environment variables or defaulting to specified values
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    # Run the Flask server with specified configurations
    app.run(host=host, port=port, threaded=True)
