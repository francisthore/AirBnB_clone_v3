#!/usr/bin/python3
"""
Main application module
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(exception):
    """
    Close storage connection when app context is torn down
    """
    storage.close()


@app.errorhandler(404)
def not_found_error(exception):
    """
    Handle 404 errors by returning a JSON response
    """
    error_response = {"error": "Not found"}
    return jsonify(error_response), 404

if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST", "0.0.0.0"),
            getenv("HBNB_API_PORT", "5000"))
