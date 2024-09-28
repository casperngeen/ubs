import json
import logging
import re

from flask import request, jsonify
from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/lab_work', methods=['POST'])
def evaluate_lab_work():
    # Get input
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    # Check if data is a list
    if not isinstance(data, list):
        return jsonify({"error": "Input data must be a list of test case strings."}), 400
    
    # Initialize a list to hold results for each test case
    all_results = []
    
    # Process each test case string
    for test_case in data:
        # Parse input
        try:
            labs, cell_counts, increments, conditions = parse_data(test_case)
        except Exception as e:
            logging.error(f"Error parsing test case: {e}")
            return jsonify({"error": "Invalid test case format."}), 400

        # Initialize result as a list of zeros for each lab
        result = [0 for _ in range(len(labs))]

        print(labs)
        print(cell_counts)
        print(increments)
        print(conditions)

        # Simulate for 1000 days
        for day in range(1000):
            temp_cell_count = [[] for _ in range(len(labs))]
            for i in range(len(labs)):
                for j in range(len(cell_counts[i])):
                    current_count = cell_counts[i][j]

                    # Increment cell_count
                    new_count = compute_count_statement(increments[i], current_count)

                    # Store result
                    result[i] += new_count

                    # Get conditions
                    divisor = conditions[i][0]
                    true_lab_index = conditions[i][1] - 1
                    false_lab_index = conditions[i][2] - 1 

                    # Check for valid lab indices
                    if true_lab_index >= len(labs) or false_lab_index >= len(labs):
                        logging.error("Invalid lab index in conditions.")
                        return jsonify({"error": "Invalid lab index in conditions."}), 400

                    # Populate next day's cell counts based on conditions
                    if new_count % divisor == 0:
                        temp_cell_count[true_lab_index].append(new_count)
                    else:
                        temp_cell_count[false_lab_index].append(new_count)
            cell_counts = temp_cell_count

        # Prepare the result for this test case
        result_dict = {"1000": result}
        all_results.append(result_dict)
        logging.info("Result for test case: {}".format(result_dict))

    # Return all results as a JSON response
    return jsonify(all_results)

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

def compute_count_statement(statement, value):
    
    # Replace 'count' with the provided value in the statement
    statement = statement.replace("count", str(value))
    
    # Use eval to compute the result of the mathematical expression
    result = eval(statement)
    
    return result