#!/usr/bin/python3
"""
This script sets up a Flask web server.
"""
import os
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """JSON formatted 404 response"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close_db(error):
    """Close storage on teardown"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
