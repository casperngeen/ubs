import logging

from flask import request, jsonify

from routes import app

logger = logging.getLogger(__name__)

@app.route('/coolcodehack', methods=['POST'])
def evaluate_coolcodehack():
    result = {
        "username": "zi xin",
        "password": "Zx@91559732"
    }
    return jsonify(result)

