from flask import request, jsonify
from collections import defaultdict, deque
import logging

from flask import request
from routes import app

logger = logging.getLogger(__name__)

@app.route('/bugfixer/p1', methods=['POST'])
def evaluate_bugfixer_p1():
    data = request.get_json()

    results = []

    for test_case in data:
        time = test_case['time']
        prerequisites = test_case['prerequisites']

        n = len(time)  # Number of projects
        graph = defaultdict(list)
        indegree = [0] * n  # In-degree of each node

        # Build the graph and in-degree array
        print(prerequisites)
        for a, b in prerequisites:
            u = a - 1  # Convert to 0-based index
            v = b - 1
            graph[u].append(v)
            indegree[v] += 1

        # Topological Sort
        queue = deque()
        dp = [t for t in time]  # Initialize dp array with the project times

        # Enqueue nodes with in-degree zero
        for i in range(n):
            if indegree[i] == 0:
                queue.append(i)

        # Process nodes in topological order
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                # Update dp[v] if a longer path is found
                if dp[v] < dp[u] + time[v]:
                    dp[v] = dp[u] + time[v]
                indegree[v] -= 1
                if indegree[v] == 0:
                    queue.append(v)

        total_time = max(dp)
        results.append(total_time)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)