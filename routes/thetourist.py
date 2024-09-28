import heapq
from collections import deque
from itertools import combinations
import json
import logging
from flask import request
from routes import app
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

LINES = {
    "Tokyo Metro Ginza Line": [
        "Asakusa", "Tawaramachi", "Inaricho", "Ueno", "Ueno-hirokoji", "Suehirocho",
        "Kanda", "Mitsukoshimae", "Nihombashi", "Kyobashi", "Ginza", "Shimbashi",
        "Toranomon", "Tameike-sanno", "Akasaka-mitsuke", "Nagatacho", "Aoyama-itchome",
        "Gaiemmae", "Omotesando", "Shibuya"
    ],
    "Tokyo Metro Marunouchi Line": [
        "Ogikubo", "Minami-asagaya", "Shin-koenji", "Higashi-koenji", "Shin-nakano",
        "Nakano-sakaue", "Nishi-shinjuku", "Shinjuku", "Shinjuku-sanchome", "Shin-ochanomizu",
        "Ochanomizu", "Awajicho", "Otemachi", "Tokyo", "Ginza", "Kasumigaseki", "Kokkai-gijidomae",
        "Akasaka-mitsuke", "Yotsuya", "Yotsuya-sanchome", "Shinjuku-gyoemmae", "Nishi-shinjuku-gochome",
        "Nakano-fujimicho", "Nakano-shimbashi", "Nakano-sakaue", "Shinjuku-sanchome", "Kokkai-gijidomae",
        "Kasumigaseki", "Ginza", "Tokyo", "Otemachi", "Awajicho", "Shin-ochanomizu", "Ochanomizu"
    ],
    "Tokyo Metro Hibiya Line": [
        "Naka-meguro", "Ebisu", "Hiroo", "Roppongi", "Kamiyacho", "Kasumigaseki", "Hibiya",
        "Ginza", "Higashi-ginza", "Tsukiji", "Hatchobori", "Kayabacho", "Nihombashi",
        "Kodemmacho", "Akihabara", "Naka-okachimachi", "Ueno", "Iriya", "Minowa",
        "Minami-senju", "Kita-senju"
    ],
    "Tokyo Metro Tozai Line": [
        "Nakano", "Ochiai", "Takadanobaba", "Waseda", "Kagurazaka", "Iidabashi", "Kudanshita",
        "Takebashi", "Otemachi", "Nihombashi", "Kayabacho", "Monzen-nakacho", "Kiba",
        "Toyosu", "Minami-sunamachi", "Nishi-kasai", "Kasai", "Urayasu", "Minami-gyotoku",
        "Gyotoku", "Myoden", "Baraki-nakayama", "Nishi-funabashi"
    ],
    "Tokyo Metro Chiyoda Line": [
        "Yoyogi-uehara", "Yoyogi-koen", "Meiji-jingumae", "Omotesando", "Nogizaka", "Akasaka",
        "Kokkai-gijidomae", "Kasumigaseki", "Hibiya", "Nijubashimae", "Otemachi",
        "Shin-ochanomizu", "Yushima", "Nezu", "Sendagi", "Nishi-nippori", "Machiya",
        "Kita-senju", "Ayase", "Kita-ayase"
    ],
    "Tokyo Metro Yurakucho Line": [
        "Wakoshi", "Chikatetsu-narimasu", "Chikatetsu-akatsuka", "Heiwadai", "Hikawadai",
        "Kotake-mukaihara", "Senkawa", "Kanamecho", "Ikebukuro", "Higashi-ikebukuro",
        "Gokokuji", "Edogawabashi", "Iidabashi", "Ichigaya", "Kojimachi", "Nagatacho",
        "Sakuradamon", "Yurakucho", "Ginza-itchome", "Shintomicho", "Toyocho",
        "Kiba", "Toyosu", "Tsukishima", "Shintomicho", "Tatsumi", "Shinonome", "Ariake"
    ],
    "Tokyo Metro Hanzomon Line": [
        "Shibuya", "Omotesando", "Aoyama-itchome", "Nagatacho", "Hanzomon", "Kudanshita",
        "Jimbocho", "Otemachi", "Mitsukoshimae", "Suitengumae", "Kiyosumi-shirakawa",
        "Sumiyoshi", "Kinshicho", "Oshiage"
    ],
    "Tokyo Metro Namboku Line": [
        "Meguro", "Shirokanedai", "Shirokane-takanawa", "Azabu-juban", "Roppongi-itchome",
        "Tameike-sanno", "Nagatacho", "Yotsuya", "Ichigaya", "Iidabashi", "Korakuen",
        "Todaimae", "Hon-komagome", "Komagome", "Nishigahara", "Oji", "Oji-kamiya",
        "Shimo", "Akabane-iwabuchi"
    ],
    "Tokyo Metro Fukutoshin Line": [
        "Wakoshi", "Chikatetsu-narimasu", "Chikatetsu-akatsuka", "Narimasu", "Shimo-akatsuka",
        "Heiwadai", "Hikawadai", "Kotake-mukaihara", "Senkawa", "Kanamecho", "Ikebukuro",
        "Zoshigaya", "Nishi-waseda", "Higashi-shinjuku", "Shinjuku-sanchome", "Kita-sando",
        "Meiji-jingumae", "Shibuya"
    ],
    "Toei Asakusa Line": [
        "Nishi-magome", "Magome", "Nakanobu", "Togoshi", "Gotanda", "Takanawadai",
        "Sengakuji", "Mita", "Shiba-koen", "Daimon", "Shimbashi", "Higashi-ginza",
        "Takaracho", "Nihombashi", "Ningyocho", "Higashi-nihombashi", "Asakusabashi",
        "Kuramae", "Asakusa", "Honjo-azumabashi", "Oshiage"
    ],
    "Toei Mita Line": [
        "Meguro", "Shirokanedai", "Shirokane-takanawa", "Mita", "Shiba-koen", "Onarimon",
        "Uchisaiwaicho", "Hibiya", "Otemachi", "Jimbocho", "Suidobashi", "Kasuga",
        "Hakusan", "Sengoku", "Sugamo", "Nishi-sugamo", "Shin-itabashi", "Itabashi-kuyakushomae",
        "Itabashi-honcho", "Motohasunuma", "Shin-takashimadaira", "Nishidai", "Hasune",
        "Takashimadaira", "Shimura-sakaue", "Shimura-sanchome", "Nishidai"
    ],
    "Toei Shinjuku Line": [
        "Shinjuku", "Shinjuku-sanchome", "Akebonobashi", "Ichigaya", "Kudanshita",
        "Jimbocho", "Ogawamachi", "Iwamotocho", "Bakuro-yokoyama", "Hamacho",
        "Morishita", "Kikukawa", "Sumiyoshi", "Nishi-ojima", "Ojima", "Higashi-ojima",
        "Funabori", "Ichinoe", "Mizue", "Shinozaki", "Motoyawata"
    ],
    "Toei Oedo Line": [
        "Hikarigaoka", "Nerima-kasugacho", "Toshimaen", "Nerima", "Nerima-sakamachi",
        "Shin-egota", "Ochiai-minami-nagasaki", "Nakai", "Higashi-nakano", "Nakano-sakaue",
        "Nishi-shinjuku-gochome", "Tochomae", "Shinjuku-nishiguchi", "Higashi-shinjuku",
        "Wakamatsu-kawada", "Ushigome-yanagicho", "Ushigome-kagurazaka", "Iidabashi",
        "Kasuga", "Hongosanchome", "Ueno-okachimachi", "Shin-okachimachi", "Kuramae",
        "Ryogoku", "Morishita", "Kiyosumi-shirakawa", "Monzen-nakacho", "Tsukishima",
        "Kachidoki", "Shiodome", "Daimon", "Akasaka-mitsuke", "Roppongi", "Aoyama-itchome",
        "Shinjuku", "Tochomae", "Shinjuku", "Shinjuku-sanchome", "Higashi-shinjuku",
        "Wakamatsu-kawada", "Ushigome-yanagicho", "Ushigome-kagurazaka", "Iidabashi",
        "Kasuga", "Hongosanchome", "Ueno-okachimachi", "Shin-okachimachi", "Kuramae",
        "Ryogoku", "Morishita", "Kiyosumi-shirakawa", "Monzen-nakacho", "Tsukishima",
        "Kachidoki", "Shiodome", "Daimon", "Shiodome", "Tsukishima"
    ]
}

LINE_TRAVEL_TIME = {
    "Tokyo Metro Ginza Line": 2,
    "Tokyo Metro Marunouchi Line": 3,
    "Tokyo Metro Hibiya Line": 2.5,
    "Tokyo Metro Tozai Line": 4,
    "Tokyo Metro Chiyoda Line": 1.5,
    "Tokyo Metro Yurakucho Line": 2,
    "Tokyo Metro Hanzomon Line": 2,
    "Tokyo Metro Namboku Line": 1,
    "Tokyo Metro Fukutoshin Line": 3,
    "Toei Asakusa Line": 3.5,
    "Toei Mita Line": 4,
    "Toei Shinjuku Line": 1.5,
    "Toei Oedo Line": 1
}

TEST_INPUT = {
    "locations": {
        "Yoyogi-uehara": [0, 0],
        "Meiji-jingumae": [12, 35],
        "Oji": [12, 30],
        "Takebashi": [15, 25],
        "Tameike-sanno": [45, 20],
        "Shimbashi": [13, 35],
        "Minami-asagaya": [22, 15]
    },
    "startingPoint": "Yoyogi-uehara",
    "timeLimit": 480
}

TEST_INPUT_2 = {'locations': {'Tokyo': [0, 0], 'Kiyosumi-shirakawa': [38, 35], 'Narimasu': [12, 25], 'Uchisaiwaicho': [42, 35], 'Kotake-mukaihara': [21, 35], 'Shinonome': [15, 25], 'Ariake': [43, 30], 'Jimbocho': [35, 20], 'Oshiage': [26, 15], 'Nakanobu': [40, 15], 'Chikatetsu-akatsuka': [40, 20], 'Itabashi-kuyakushomae': [35, 15], 'Baraki-nakayama': [27, 35], 'Motohasunuma': [42, 20], 'Minami-gyotoku': [39, 30], 'Nishi-kasai': [28, 15], 'Ueno-okachimachi': [17, 20], 'Shirokanedai': [10, 25], 'Hikarigaoka': [30, 15], 'Akasaka-mitsuke': [44, 20], 'Mita': [13, 30], 'Meiji-jingumae': [39, 15], 'Roppongi': [31, 35], 'Urayasu': [44, 30], 'Monzen-nakacho': [35, 20], 'Kudanshita': [26, 25], 'Yotsuya': [28, 15], 'Gaiemmae': [45, 20], 'Nogizaka': [12, 35], 'Kasai': [20, 15], 'Akihabara': [42, 20], 'Waseda': [38, 25], 'Nakano-fujimicho': [23, 35], 'Kiba': [25, 15], 'Heiwadai': [17, 35], 'Asakusabashi': [15, 30], 'Hatchobori': [45, 20], 'Kyobashi': [10, 25], 'Shiba-koen': [38, 25], 'Shin-ochanomizu': [
    22, 30], 'Nishi-shinjuku-gochome': [20, 35], 'Higashi-nakano': [14, 35], 'Akebonobashi': [15, 25], 'Oji': [22, 35], 'Nijubashimae': [11, 20], 'Yurakucho': [39, 15], 'Shimbashi': [34, 30], 'Azabu-juban': [32, 35], 'Kanda': [43, 35], 'Shinjuku-nishiguchi': [17, 30], 'Togoshi': [36, 15], 'Shimo-akatsuka': [27, 25], 'Kokkai-gijidomae': [43, 25], 'Nishi-ojima': [34, 30], 'Ichinoe': [11, 30], 'Toyosu': [19, 25], 'Nakai': [36, 15], 'Awajicho': [44, 30], 'Ryogoku': [14, 35], 'Sendagi': [21, 35], 'Tsukiji': [28, 25], 'Hongosanchome': [37, 35], 'Akasaka': [14, 15], 'Toshimaen': [26, 35], 'Minami-senju': [24, 20], 'Hakusan': [27, 35], 'Nerima': [35, 25], 'Shiodome': [41, 15], 'Shimura-sanchome': [30, 30], 'Ochiai': [14, 20], 'Onarimon': [30, 30], 'Nakano-sakaue': [28, 15], 'Tochomae': [36, 20], 'Wakoshi': [34, 35], 'Tameike-sanno': [21, 25], 'Nishi-nippori': [19, 15], 'Kasuga': [40, 30], 'Magome': [21, 25], 'Nishigahara': [28, 15], 'Asakusa': [29, 35], 'Higashi-ginza': [16, 25]}, 'startingPoint': 'Tokyo', 'timeLimit': 480}


class Node:
    def __init__(self, value):
        self.value = value
        self.edges = []  # List of edges as (node, weight) tuples

    def add_edge(self, node, weight):
        # Avoid adding duplicate edges with the same weight
        if not any(edge[0].value == node.value and edge[1] == weight for edge in self.edges):
            self.edges.append((node, weight))  # Store edge with weight
    def __repr__(self):
        return f'Node({self.value})'


class Graph:
    def __init__(self):
        self.nodes = {}

    def get_node(self, value):
        return self.nodes[value]

    def get_node(self, value):
        return self.nodes[value]

    def add_node(self, value):
        if value not in self.nodes:
            new_node = Node(value)
            self.nodes[value] = new_node
        else:
            print(f'Node {value} already exists.')

    def add_edge(self, from_value, to_value, weight):
        if from_value in self.nodes and to_value in self.nodes:
            # Add edge from from_value to to_value
            self.nodes[from_value].add_edge(self.nodes[to_value], weight)
            # Add edge from to_value to from_value (making it bidirectional)
            self.nodes[to_value].add_edge(self.nodes[from_value], weight)
        else:
           print(f'One or both nodes not found: {from_value}, {to_value}')

    def display(self):
        for node in self.nodes.values():
            edges = [(edge[0].value, edge[1])
                     for edge in node.edges]  # Extract node value and weight
            print(f'{node.value} -> {edges}')

    def dijkstra(self, start, subgraph):
        # Priority queue for Dijkstra's algorithm
        priority_queue = []
        heapq.heappush(priority_queue, (0, start))  # (weight, start)
        visited = set()
        distances = {node: float('inf')
                     for node in self.nodes}  # Initialize distances
        visited.add(start)
        distances[start] = 0

        while priority_queue:
            current_distance, current_node_value = heapq.heappop(priority_queue)
            if current_node_value in subgraph.nodes:
                visited.add(current_node_value)
                if len(visited) == len(subgraph.nodes):
                    break
            current_node = self.nodes[current_node_value]
            # Explore neighbors
            for neighbor, weight in current_node.edges:
                distance = current_distance + weight

                # Only consider this new path if it's better
                if distance < distances[neighbor.value]:
                    distances[neighbor.value] = distance
                    heapq.heappush(priority_queue, (distance, neighbor.value))
        for node in list(distances.keys()):
            if node not in subgraph.nodes:
                distances.pop(node)
        return distances

    def create_complete_subgraph(self, node_values):
        """
        Creates a complete subgraph where every node in node_values is connected to every other node.
        The weight of each edge is the shortest distance between the two nodes in the original graph.

        :param node_values: List of node values to include in the subgraph
        :return: A new Graph instance representing the complete subgraph
        """
        # Verify all nodes exist in the original graph
        for value in node_values:
            if value not in self.nodes:
                raise ValueError(f'Node {value} does not exist in the graph.')

        # Initialize the subgraph
        subgraph = Graph()
        for value in node_values:
            subgraph.add_node(value)
        print(f"{subgraph.nodes}")

        # Generate all unique pairs of nodes
        for node in node_values:
            result = self.dijkstra(node, subgraph)
            # Add edge with the shortest distance
            for neighbour in result:
                if (neighbour, result[neighbour]) not in subgraph.get_node(node).edges:
                    subgraph.add_edge(node, neighbour, result[neighbour])
        return subgraph

def construct_graph(lines, line_travel_time):
    graph = Graph()
    for line_name, stations in lines.items():
        if not stations:
            continue  # Skip empty station lists

        # Add the first station if it doesn't exist
        first_station = stations[0]
        if first_station not in graph.nodes:
            graph.add_node(first_station)

        prevStation = first_station

        for station in stations[1:]:
            if station not in graph.nodes:
                graph.add_node(station)
            graph.add_edge(station, prevStation, line_travel_time[line_name])
            prevStation = station

    return graph


@app.route('/tourist', methods=['POST'])
def tourist():
    input = request.get_json()
    logging.info("data sent for evaluation {}".format(input))

    location, starting_point, time_limit = input.get(
        "locations"), input.get("startingPoint"), input.get("timeLimit")
    full_graph = construct_graph(LINES, LINE_TRAVEL_TIME)
    complete_subgraph = full_graph.create_complete_subgraph(
        list(location.keys()))

    # (currNode, currPath, currCost, currReward, visitedNodes)
    queue = deque([(station,
                    [starting_point, station.value],
                    cost + location[station.value][1],
                    location[station.value][0],
                    set([station.value])) for station, cost in complete_subgraph.nodes[starting_point].edges])

    currBestPath = []
    currMaxReward = -1

    while queue:
        currNode, currPath, currCost, currReward, visitedNodes = queue.popleft()
        if currCost > time_limit:
            continue
        if currNode.value == starting_point:
            if currReward > currMaxReward:
                currBestPath = currPath
                currMaxReward = currReward
            continue
        for nextNode, weight in currNode.edges:
            if nextNode.value not in visitedNodes:
                queue.append((nextNode,
                              currPath + [nextNode.value],
                              currCost + location[nextNode.value][1] + weight,
                              currReward + location[nextNode.value][0],
                              visitedNodes.union({nextNode.value})))

    return currBestPath, currMaxReward

#@app.route('/tourist', methods=['POST'])
def evaluate_tourist():
    input_data = request.get_json()

    locations = input_data["locations"]
    starting_point = input_data["startingPoint"]
    time_limit = input_data["timeLimit"]
    
    memo = {}

    # Helper function with memoization
    def find_optimal_path(current_station, remaining_time, path, total_satisfaction):
        # Base case: if we run out of time, return satisfaction so far
        if remaining_time < 0:
            return -1, path  # Exceeded time
        if current_station == starting_point and len(path) > 1:
            return total_satisfaction, path  # Return satisfaction if back at start

        # Memoization: avoid recalculating for the same state
        state = (current_station, remaining_time, tuple(path))
        if state in memo:
            return memo[state]

        max_satisfaction = total_satisfaction
        best_path = path[:]

        # Try visiting each station that hasn't been visited yet
        for station, (satisfaction, time_needed) in locations.items():
            if station not in path:
                # Only proceed if we can still visit this station within the time limit
                new_time = remaining_time - time_needed
                if new_time >= 0:
                    new_satisfaction, new_path = find_optimal_path(
                        station, new_time, path + [station], total_satisfaction + satisfaction
                    )
                    # Update if we find a better satisfaction path
                    if new_satisfaction > max_satisfaction:
                        max_satisfaction = new_satisfaction
                        best_path = new_path

        # Memoize the result, store both satisfaction and path
        memo[state] = (max_satisfaction, best_path)
        return max_satisfaction, best_path

    # Start the recursive search from the starting point
    total_satisfaction, best_path = find_optimal_path(starting_point, time_limit, [starting_point], 0)

    # Output the best path and total satisfaction
    return {'path': best_path, 'satisfaction': total_satisfaction}