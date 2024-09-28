import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

@app.route('/dodge', methods=['POST'])
def evaluate_dodge():
    data = request.get_json()
    app.logger.info("Data received for evaluation: %s", data)
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
