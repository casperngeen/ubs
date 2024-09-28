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
        dp0 = [None for _ in range(len(monsters))]
        dp1 = [None for _ in range(len(monsters))]

        dict = {}
        dict["efficiency"] = helper(0, 0, dp0, dp1, monsters) 
        results.append(dict)

    return jsonify(results)

#state: 0 is no mana, 1 is charged up
def helper(state, time, dp0, dp1, monsters):
    if state == 0:
        # Base case
        if len(monsters) - 1 == time:
            return 0
        
        # dp
        if dp0[time] != None:
            return dp0[time]
        
        # Recursive step 
        case1 = helper(0, time + 1, dp0, dp1, monsters) # move back
        case2 = -monsters[time] + helper(1, time + 1, dp0, dp1, monsters) # recharge
        dp0[time] = max(case1, case2)
        return dp0[time]
    
    if state == 1:
        # Base case
        if len(monsters) - 1 == time:
            return monsters[time]
        
        # dp
        if dp1[time] != None:
            return dp1[time]
        
        # Recursive step 
        case1 = helper(1, time + 1, dp0, dp1, monsters) # move back
        case2 = monsters[time] + helper(0, time + 1, dp0, dp1, monsters) # attack
        dp1[time] = max(case1, case2)
        return dp1[time]

if __name__ == '__main__':
    app.run(debug=True)    


                
