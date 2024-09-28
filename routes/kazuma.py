import logging

from flask import request, jsonify

from routes import app

logger = logging.getLogger(__name__)

@app.route('/efficient-hunter-kazuma', methods=['POST'])
def evaluate_kazuma():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    results = []
    for test_case in data:
        monsters = test_case["monsters"]
        dp = {} 

        dict = {}
        dict["efficiency"] = helper(0, 0, dp, monsters, 0) # tuple of (time, state, prev)
        results.append(dict)

    return jsonify(results)

#state: 0 is no mana, 1 is charged up
def helper(state, time, dp, monsters, prev):
    if state == 0:
        # Base case
        if len(monsters) - 1 == time:
            return 0
        
        # dp
        if dp.get((time, state, prev), None) != None:
            return dp[(time, state, prev)]
        
        # Recursive step 
        case1 = helper(0, time + 1, dp, monsters, 0) # move back
        case2 = 0
        if prev == 0:
            case2 = -monsters[time] + helper(1, time + 1, dp, monsters, 0) # recharge
        dp[(time, state, prev)] = max(case1, case2)
        return dp[(time, state, prev)]
    
    if state == 1:
        # Base case
        if len(monsters) - 1 == time:
            return monsters[time]
        
         # dp
        if dp.get((time, state, prev), None) != None:
            return dp.get((time, state, prev))
        
        # Recursive step 
        case1 = helper(1, time + 1, dp, monsters, 0) # move back
        case2 = monsters[time] + helper(0, time + 1, dp, monsters, 1) # attack
        dp[(time, state, prev)] = max(case1, case2)
        return dp[(time, state, prev)]

if __name__ == '__main__':
    app.run(debug=True)    


                
