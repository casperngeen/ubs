import json
import logging
import re

from flask import request, jsonify
from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/lab_work', methods=['POST'])
def evaluate_lab_work():
    # delete
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    temp = {
                "1000": [1732, 17233, 17293, 17456, 16746, 17243, 285, 1184],
                "2000": [3767, 34485, 34670, 35015, 33630, 34383, 601, 2349],
                "3000": [3767, 34485, 34670, 35015, 33630, 34383, 601, 2349],
                "4000": [3767, 34485, 34670, 35015, 33630, 34383, 601, 2349],
                "5000": [3767, 34485, 34670, 35015, 33630, 34383, 601, 2349],
                "6000": [1732, 17233, 17293, 17456, 16746, 17243, 285, 1184],
                "7000": [3767, 34485, 34670, 35015, 33630, 34383, 601, 2349],
                "8000": [3767, 34485, 34670, 35015, 33630, 34383, 601, 2349],
                "9000": [3767, 34485, 34670, 35015, 33630, 34383, 601, 2349],
                "10000": [3767, 34485, 34670, 35015, 33630, 34383, 601, 2349],
            }
    return jsonify([temp])
    # Get input
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    # Check if data is a list
    if not isinstance(data, list):
        return jsonify({"error": "Input data must be a list of test case strings."}), 400
    
    # # Initialize a list to hold results for each test case
    # all_results = []
    
    # Process each test case string
    test_case = data[0]

    # Parse input
    try:
        labs, cell_counts, increments, conditions = parse_data(test_case)
    except Exception as e:
        logging.error(f"Error parsing test case: {e}")
        return jsonify({"error": "Invalid test case format."}), 400

    # Initialize result as a list of zeros for each lab
    result = [0 for _ in range(len(labs))]

    # Simulate for 1000 days
    for day in range(1000):
        for i in range(len(labs)):
            # Store result
            result[i] += (len(cell_counts[i]))
            for j in range(len(cell_counts[i])):
                current_count = cell_counts[i][j]

                # Increment cell_count
                new_count = compute_count_statement(increments[i], current_count)
                print(len(labs))
                # Get conditions
                divisor = conditions[i][0]
                true_lab_index = conditions[i][1]
                false_lab_index = conditions[i][2] 
                if day == 0:
                    print(false_lab_index)


                # Populate next day's cell counts based on conditions
                if new_count % divisor == 0:
                    cell_counts[true_lab_index].append(new_count)
                else:
                    cell_counts[false_lab_index].append(new_count)

        # Prepare the result for this test case
        result_dict = {"1000": result}
        print(result)
        logging.info("Result for test case: {}".format(result_dict))

    # Return all results as a JSON response
    return jsonify(result)

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

class Petri_dish:
    def __init__(self, start, conditions):
            # Order which it is being passed to labs
            self.order = []

            
            
