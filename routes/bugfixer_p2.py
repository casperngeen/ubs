from flask import request, jsonify
import heapq
import logging

from flask import request
from routes import app

logger = logging.getLogger(__name__)

@app.route('/bugfixer/p2', methods=['POST'])
def bugfixer_p2():
    data = request.get_json()

    results = []

    for test_case in data:
        bugseq = test_case['bugseq']
        # Each bug is [difficulty, limit]

        # Sort the bugs by their limits (deadlines)
        bugs = sorted(bugseq, key=lambda x: x[1])

        total_time = 0
        max_heap = []  # Using negative durations to simulate a max-heap

        for bug in bugs:
            duration = bug[0]
            limit = bug[1]
            total_time += duration
            # Push negative duration to simulate max-heap behavior
            heapq.heappush(max_heap, -duration)
            if total_time > limit:
                # Remove the bug with the largest duration
                removed_duration = -heapq.heappop(max_heap)
                total_time -= removed_duration

        max_bugs_fixed = len(max_heap)
        results.append(max_bugs_fixed)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)