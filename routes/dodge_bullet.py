import logging
from flask import request, jsonify

from routes import app

logger = logging.getLogger(__name__)

@app.route('/dodge', methods=['POST'])
def evaluate_dodge():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)   
