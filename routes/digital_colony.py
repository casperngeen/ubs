import logging

from flask import request, json

from routes import app

logger = logging.getLogger(__name__)

@app.route('/digital-colony', methods=['POST'])
def evaluate_digital_colony():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    results = []
    for test_case in data:
        generations = test_case["generations"]
        colony = test_case["colony"]
        
        weight = sum(int(digit) for digit in colony)
        pairs = {key: 0 for key in range(100)}
        for i in range(len(colony)-1):
            key = int(colony[i])*10 + int(colony[i+1])
            pairs[key] += 1
        for _ in range(generations):
            new_weight = weight
            new_pairs = {key: 0 for key in range(100)}
            for key in pairs:
                if pairs[key] == 0:
                    continue
                first = key // 10
                second = key % 10
                signature = 0
                if first > second:
                    signature = first - second
                elif second > first:
                    signature = 10 - (second-first)
                new_digit = (signature + weight) % 10
                new_weight += new_digit * pairs[key]
                key1 = first*10+new_digit
                key2 = new_digit*10+second
                new_pairs[key1] += pairs[key]
                new_pairs[key2] += pairs[key]
            weight = new_weight
            pairs = new_pairs
        results.append(str(weight))


        '''
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
        '''
    return json.dumps(results) 


                
