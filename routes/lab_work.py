import json
import logging
import re

from flask import request, jsonify
from flask import request

from routes import app
import sys

# Disable the limit on integer string conversion digits
sys.set_int_max_str_digits(0)

logger = logging.getLogger(__name__)


@app.route('/lab_work', methods=['POST'])
def evaluate_lab_work():
    
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
                cell_counts[i][j] = compute_count_statement(increments[i], cell_counts[i][j])

                # Get conditions
                divisor = conditions[i][0]
                true_lab_index = conditions[i][1]
                false_lab_index = conditions[i][2] 

                # Populate next day's cell counts based on conditions
                if cell_counts[i][j] % divisor == 0:
                    cell_counts[true_lab_index].append(cell_counts[i][j])
                else:
                    cell_counts[false_lab_index].append(cell_counts[i][j])
                
            cell_counts[i] = []

        # Prepare the result for this test case
        result_dict = {"1000": result}
    

    # Return all results as a JSON response
    return jsonify(result_dict)

def parse_data(raw_data):
    # Use regex to capture each row of the table
    pattern = r'\|(\d+)\s+\|\s+([\d\s]+)\s+\|\s+([^\|]+)\s+\|\s+([\d\s]+)\s+\|'
    matches = re.findall(pattern, raw_data)
    
    # Prepare lists for each column
    labs = []
    current_counts = []
    increments = []
    conditions = []
    
    # Process each match and populate the lists
    for match in matches:
        lab, counts, increment, condition = match
        labs.append(int(lab.strip()))
        current_counts.append(list(map(int, counts.split())))
        increments.append(increment.strip())
        conditions.append(list(map(int, condition.split())))
    
    return labs, current_counts, increments, conditions

def compute_count_statement(statement, value):
    
    # # Replace 'count' with the provided value in the statement
    # statement = statement.replace("count", str(value))
    
    # # Use eval to compute the result of the mathematical expression
    # result = eval(statement)

    # return result

    # Remove any spaces for easier processing
    statement = statement.replace(" ", "")
    
    if '*' in statement:
        if 'count*count' in statement:
            return bitwise_multiply(value, value)  # Special case for 'count * count'
        else:
            factor = int(statement.split('*')[1])
            return bitwise_multiply(value, factor)
    
    elif '+' in statement:
        if 'count+count' in statement:
            return bitwise_add(value, value)  # Special case for 'count + count'
        else:
            addend = int(statement.split('+')[1])
            return bitwise_add(value, addend)
    
    else:
        raise ValueError(f"Unsupported increment statement: {statement}")
    
def bitwise_multiply(a, b):
    result = 0
    while b > 0:
        if b & 1:  # If the least significant bit of b is 1
            result = bitwise_add(result, a)
        a <<= 1  # Left shift a by 1 (multiply by 2)
        b >>= 1  # Right shift b by 1 (divide by 2)
    return result

def bitwise_add(a, b):
    while b != 0:
        carry = a & b
        a = a ^ b
        b = carry << 1
    return a

def bitwise_modulo(a, b):
    # Works if b is a power of 2, i.e., b = 2^n
    return a & (b - 1)

            
            
