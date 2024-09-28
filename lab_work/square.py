import json
import logging
import re

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/lab_work', methods=['POST'])
def evaluate_lab_work():
    # Get input
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    input_value = data.get("input")

    # Parse input
    labs, cell_counts, increments, conditions = parse_data(input_value)

    result = [0 for _ in range(len(labs))]
    for day in range(1000):
        temp_cell_count = [[] for _ in range(len(labs))]
        for i in range(len(labs)):
            for j in range(len(cell_counts[i])):
                # Increment cell_count
                new_count = compute_count_statement(increments[i], cell_counts[i][j])
                
                # Store result
                result[i] += new_count

                # populate next day cell count
                if cell_counts[i][j] % conditions[0] == 0:
                    temp_cell_count[conditions[1]].append(cell_counts[i][j])
                else:
                    temp_cell_count[conditions[2]].append(cell_counts[i][j])
        cell_counts = temp_cell_count

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

def compute_count_statement(statement, value):
    
    # Replace 'count' with the provided value in the statement
    statement = statement.replace("count", str(value))
    
    # Use eval to compute the result of the mathematical expression
    result = eval(statement)
    
    return result