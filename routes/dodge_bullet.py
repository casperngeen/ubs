import logging

from flask import request, jsonify

from routes import app

logger = logging.getLogger(__name__)

@app.route('/dodge', methods=['POST'])
def evaluate_dodge():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    results = []
    for test_case in data:
        generations = test_case["generations"]
        colony = test_case["colony"]

        # Solve for only generation 10 :(
        generations = 10

        while generations > 0:
            next_colony_arr = ['_' for _ in range(len(colony) * 2 - 1)]
            curr_colony_index_counter = 0
            new_colony_index_counter = 1
            print(colony)
            for i in range(len(colony) - 1):
                weight = sum(int(digit) for digit in colony)
                next_colony_arr[new_colony_index_counter] = str((weight + (int(colony[i]) - int(colony[i + 1]))) % 10)
                next_colony_arr[curr_colony_index_counter] = colony[i]
                next_colony_arr[curr_colony_index_counter + 2] = colony[i + 1]
                new_colony_index_counter += 2
                curr_colony_index_counter += 2
            colony = ''.join(next_colony_arr)
            generations -= 1
        results.append(sum(int(digit) for digit in colony))

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)    


                

