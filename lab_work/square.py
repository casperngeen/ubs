import json
import logging
import re

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/square', methods=['POST'])
def evaluate():
    # Get input
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    input_value = data.get("input")

    # Parse input
    parse_data()


    # Return Result
    result = input_value * input_value
    logging.info("My result :{}".format(result))
    return json.dumps(result)

def parse_data(raw_data):
    labs = []
    cell_counts = []
    increments = []
    conditions = []

    # Use regex to parse each row
    pattern = r"\|(\d+)\s*\|\s*([\d\s]+)\s*\|\s*(count [\*\+\d\s]+)\s*\|\s*([\d\s]+)\s*\|"
    matches = re.findall(pattern, raw_data)

    # Extract parsed data into lists
    for match in matches:
        labs.append(int(match[0]))  # Lab number
        cell_counts.append([int(x) for x in match[1].split()])  # Cell counts as an array of integers
        increments.append(match[2].strip())  # Increment (as a string)
        conditions.append([int(x) for x in match[3].split()])  # Condition as an array of integers

    return labs, cell_counts, increments, conditions