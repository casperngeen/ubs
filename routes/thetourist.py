# import heapq
# from collections import deque
# from itertools import combinations

# LINES = {
#     "Tokyo Metro Ginza Line": [
#         "Asakusa", "Tawaramachi", "Inaricho", "Ueno", "Ueno-hirokoji", "Suehirocho",
#         "Kanda", "Mitsukoshimae", "Nihombashi", "Kyobashi", "Ginza", "Shimbashi",
#         "Toranomon", "Tameike-sanno", "Akasaka-mitsuke", "Nagatacho", "Aoyama-itchome",
#         "Gaiemmae", "Omotesando", "Shibuya"
#     ],
#     "Tokyo Metro Marunouchi Line": [
#         "Ogikubo", "Minami-asagaya", "Shin-koenji", "Higashi-koenji", "Shin-nakano",
#         "Nakano-sakaue", "Nishi-shinjuku", "Shinjuku", "Shinjuku-sanchome", "Shin-ochanomizu",
#         "Ochanomizu", "Awajicho", "Otemachi", "Tokyo", "Ginza", "Kasumigaseki", "Kokkai-gijidomae",
#         "Akasaka-mitsuke", "Yotsuya", "Yotsuya-sanchome", "Shinjuku-gyoemmae", "Nishi-shinjuku-gochome",
#         "Nakano-fujimicho", "Nakano-shimbashi", "Nakano-sakaue", "Shinjuku-sanchome", "Kokkai-gijidomae",
#         "Kasumigaseki", "Ginza", "Tokyo", "Otemachi", "Awajicho", "Shin-ochanomizu", "Ochanomizu"
#     ],
#     "Tokyo Metro Hibiya Line": [
#         "Naka-meguro", "Ebisu", "Hiroo", "Roppongi", "Kamiyacho", "Kasumigaseki", "Hibiya",
#         "Ginza", "Higashi-ginza", "Tsukiji", "Hatchobori", "Kayabacho", "Nihombashi",
#         "Kodemmacho", "Akihabara", "Naka-okachimachi", "Ueno", "Iriya", "Minowa",
#         "Minami-senju", "Kita-senju"
#     ],
#     "Tokyo Metro Tozai Line": [
#         "Nakano", "Ochiai", "Takadanobaba", "Waseda", "Kagurazaka", "Iidabashi", "Kudanshita",
#         "Takebashi", "Otemachi", "Nihombashi", "Kayabacho", "Monzen-nakacho", "Kiba",
#         "Toyosu", "Minami-sunamachi", "Nishi-kasai", "Kasai", "Urayasu", "Minami-gyotoku",
#         "Gyotoku", "Myoden", "Baraki-nakayama", "Nishi-funabashi"
#     ],
#     "Tokyo Metro Chiyoda Line": [
#         "Yoyogi-uehara", "Yoyogi-koen", "Meiji-jingumae", "Omotesando", "Nogizaka", "Akasaka",
#         "Kokkai-gijidomae", "Kasumigaseki", "Hibiya", "Nijubashimae", "Otemachi",
#         "Shin-ochanomizu", "Yushima", "Nezu", "Sendagi", "Nishi-nippori", "Machiya",
#         "Kita-senju", "Ayase", "Kita-ayase"
#     ],
#     "Tokyo Metro Yurakucho Line": [
#         "Wakoshi", "Chikatetsu-narimasu", "Chikatetsu-akatsuka", "Heiwadai", "Hikawadai",
#         "Kotake-mukaihara", "Senkawa", "Kanamecho", "Ikebukuro", "Higashi-ikebukuro",
#         "Gokokuji", "Edogawabashi", "Iidabashi", "Ichigaya", "Kojimachi", "Nagatacho",
#         "Sakuradamon", "Yurakucho", "Ginza-itchome", "Shintomicho", "Toyocho",
#         "Kiba", "Toyosu", "Tsukishima", "Shintomicho", "Tatsumi", "Shinonome", "Ariake"
#     ],
#     "Tokyo Metro Hanzomon Line": [
#         "Shibuya", "Omotesando", "Aoyama-itchome", "Nagatacho", "Hanzomon", "Kudanshita",
#         "Jimbocho", "Otemachi", "Mitsukoshimae", "Suitengumae", "Kiyosumi-shirakawa",
#         "Sumiyoshi", "Kinshicho", "Oshiage"
#     ],
#     "Tokyo Metro Namboku Line": [
#         "Meguro", "Shirokanedai", "Shirokane-takanawa", "Azabu-juban", "Roppongi-itchome",
#         "Tameike-sanno", "Nagatacho", "Yotsuya", "Ichigaya", "Iidabashi", "Korakuen",
#         "Todaimae", "Hon-komagome", "Komagome", "Nishigahara", "Oji", "Oji-kamiya",
#         "Shimo", "Akabane-iwabuchi"
#     ],
#     "Tokyo Metro Fukutoshin Line": [
#         "Wakoshi", "Chikatetsu-narimasu", "Chikatetsu-akatsuka", "Narimasu", "Shimo-akatsuka",
#         "Heiwadai", "Hikawadai", "Kotake-mukaihara", "Senkawa", "Kanamecho", "Ikebukuro",
#         "Zoshigaya", "Nishi-waseda", "Higashi-shinjuku", "Shinjuku-sanchome", "Kita-sando",
#         "Meiji-jingumae", "Shibuya"
#     ],
#     "Toei Asakusa Line": [
#         "Nishi-magome", "Magome", "Nakanobu", "Togoshi", "Gotanda", "Takanawadai",
#         "Sengakuji", "Mita", "Shiba-koen", "Daimon", "Shimbashi", "Higashi-ginza",
#         "Takaracho", "Nihombashi", "Ningyocho", "Higashi-nihombashi", "Asakusabashi",
#         "Kuramae", "Asakusa", "Honjo-azumabashi", "Oshiage"
#     ],
#     "Toei Mita Line": [
#         "Meguro", "Shirokanedai", "Shirokane-takanawa", "Mita", "Shiba-koen", "Onarimon",
#         "Uchisaiwaicho", "Hibiya", "Otemachi", "Jimbocho", "Suidobashi", "Kasuga",
#         "Hakusan", "Sengoku", "Sugamo", "Nishi-sugamo", "Shin-itabashi", "Itabashi-kuyakushomae",
#         "Itabashi-honcho", "Motohasunuma", "Shin-takashimadaira", "Nishidai", "Hasune",
#         "Takashimadaira", "Shimura-sakaue", "Shimura-sanchome", "Nishidai"
#     ],
#     "Toei Shinjuku Line": [
#         "Shinjuku", "Shinjuku-sanchome", "Akebonobashi", "Ichigaya", "Kudanshita",
#         "Jimbocho", "Ogawamachi", "Iwamotocho", "Bakuro-yokoyama", "Hamacho",
#         "Morishita", "Kikukawa", "Sumiyoshi", "Nishi-ojima", "Ojima", "Higashi-ojima",
#         "Funabori", "Ichinoe", "Mizue", "Shinozaki", "Motoyawata"
#     ],
#     "Toei Oedo Line": [
#         "Hikarigaoka", "Nerima-kasugacho", "Toshimaen", "Nerima", "Nerima-sakamachi",
#         "Shin-egota", "Ochiai-minami-nagasaki", "Nakai", "Higashi-nakano", "Nakano-sakaue",
#         "Nishi-shinjuku-gochome", "Tochomae", "Shinjuku-nishiguchi", "Higashi-shinjuku",
#         "Wakamatsu-kawada", "Ushigome-yanagicho", "Ushigome-kagurazaka", "Iidabashi",
#         "Kasuga", "Hongosanchome", "Ueno-okachimachi", "Shin-okachimachi", "Kuramae",
#         "Ryogoku", "Morishita", "Kiyosumi-shirakawa", "Monzen-nakacho", "Tsukishima",
#         "Kachidoki", "Shiodome", "Daimon", "Akasaka-mitsuke", "Roppongi", "Aoyama-itchome",
#         "Shinjuku", "Tochomae", "Shinjuku", "Shinjuku-sanchome", "Higashi-shinjuku",
#         "Wakamatsu-kawada", "Ushigome-yanagicho", "Ushigome-kagurazaka", "Iidabashi",
#         "Kasuga", "Hongosanchome", "Ueno-okachimachi", "Shin-okachimachi", "Kuramae",
#         "Ryogoku", "Morishita", "Kiyosumi-shirakawa", "Monzen-nakacho", "Tsukishima",
#         "Kachidoki", "Shiodome", "Daimon", "Shiodome", "Tsukishima"
#     ]
# }

# LINE_TRAVEL_TIME = {
#     "Tokyo Metro Ginza Line": 2,
#     "Tokyo Metro Marunouchi Line": 3,
#     "Tokyo Metro Hibiya Line": 2.5,
#     "Tokyo Metro Tozai Line": 4,
#     "Tokyo Metro Chiyoda Line": 1.5,
#     "Tokyo Metro Yurakucho Line": 2,
#     "Tokyo Metro Hanzomon Line": 2,
#     "Tokyo Metro Namboku Line": 1,
#     "Tokyo Metro Fukutoshin Line": 3,
#     "Toei Asakusa Line": 3.5,
#     "Toei Mita Line": 4,
#     "Toei Shinjuku Line": 1.5,
#     "Toei Oedo Line": 1
# }

# TEST_INPUT = {
#     "locations": {
#         "Yoyogi-uehara": [0, 0],
#         "Meiji-jingumae": [12, 35],
#         "Oji": [12, 30],
#         "Takebashi": [15, 25],
#         "Tameike-sanno": [45, 20],
#         "Shimbashi": [13, 35],
#         "Minami-asagaya": [22, 15]
#     },
#     "startingPoint": "Yoyogi-uehara",
#     "timeLimit": 480
# }


# class Node:
#     def __init__(self, value):
#         self.value = value
#         self.edges = []  # List of edges as (node, weight) tuples

#     def add_edge(self, node, weight):
#         # Avoid adding duplicate edges with the same weight
#         if not any(edge[0].value == node.value and edge[1] == weight for edge in self.edges):
#             self.edges.append((node, weight))  # Store edge with weight
#     def __repr__(self):
#         return f'Node({self.value})'


# class Graph:
#     def __init__(self):
#         self.nodes = {}

#     def get_node(self, value):
#         return self.nodes[value]

#     def add_node(self, value):
#         if value not in self.nodes:
#             new_node = Node(value)
#             self.nodes[value] = new_node
#         else:
#             print(f'Node {value} already exists.')

#     def add_edge(self, from_value, to_value, weight):
#         if from_value in self.nodes and to_value in self.nodes:
#             # Add edge from from_value to to_value
#             self.nodes[from_value].add_edge(self.nodes[to_value], weight)
#             # Add edge from to_value to from_value (making it bidirectional)
#             self.nodes[to_value].add_edge(self.nodes[from_value], weight)
#         else:
#            print(f'One or both nodes not found: {from_value}, {to_value}')

#     def display(self):
#         for node in self.nodes.values():
#             edges = [(edge[0].value, edge[1])
#                      for edge in node.edges]  # Extract node value and weight
#             print(f'{node.value} -> {edges}')

#     def dijkstra(self, start: Node):
#         # Priority queue for Dijkstra's algorithm
#         priority_queue = []
#         heapq.heappush(priority_queue, (0, start.value))  # (weight, start)
#         distances = {node: float('inf')
#                      for node in self.nodes}  # Initialize distances
#         distances[start] = 0

#         while priority_queue:
#             current_distance, current_node_value = heapq.heappop(priority_queue)
#             if current_node_value in subgraph.nodes:
#                 visited.add(current_node_value)
#                 if len(visited) == len(subgraph.nodes):
#                     break
#             current_node = self.nodes[current_node_value]

#             # Explore neighbors
#             for neighbor, weight in current_node.edges:
#                 distance = current_distance + weight

#                 # Only consider this new path if it's better
#                 if distance < distances[neighbor.value]:
#                     distances[neighbor.value] = distance
#                     previous_nodes[neighbor.value] = current_node_value
#                     heapq.heappush(priority_queue, (distance, neighbor.value))
#         return distances

#     def create_complete_subgraph(self, node_values):
#         """
#         Creates a complete subgraph where every node in node_values is connected to every other node.
#         The weight of each edge is the shortest distance between the two nodes in the original graph.

#         :param node_values: List of node values to include in the subgraph
#         :return: A new Graph instance representing the complete subgraph
#         """
#         # Verify all nodes exist in the original graph
#         for value in node_values:
#             if value not in self.nodes:
#                 raise ValueError(f'Node {value} does not exist in the graph.')

#         # Initialize the subgraph
#         subgraph = Graph()
#         for value in node_values:
#             subgraph.add_node(value)
#         print(f"{subgraph.nodes}")

#         # Generate all unique pairs of nodes
#         for node in node_values:
#             result = self.dijkstra(self.get_node(node))
#             # Add edge with the shortest distance
#             for neighbour in result:
#                 if (neighbour, result[neighbour]) not in subgraph.get_node(node).edges:
#                     subgraph.add_edge(node, neighbour, result[neighbour])
#         return subgraph

# def construct_graph(lines, line_travel_time):
#     graph = Graph()
#     for line_name, stations in lines.items():
#         if not stations:
#             continue  # Skip empty station lists

#         # Add the first station if it doesn't exist
#         first_station = stations[0]
#         if first_station not in graph.nodes:
#             graph.add_node(first_station)

#         prevStation = first_station

#         for station in stations[1:]:
#             if station not in graph.nodes:
#                 graph.add_node(station)
#             graph.add_edge(station, prevStation, line_travel_time[line_name])
#             prevStation = station

#     return graph


# @app.route('/tourist', methods=['POST'])
# def tourist():
#     input = request.get_json()
#     logging.info("data sent for evaluation {}".format(input))

#     location, starting_point, time_limit = input.get(
#         "locations"), input.get("startingPoint"), input.get("timeLimit")
#     full_graph = construct_graph(LINES, LINE_TRAVEL_TIME)
#     complete_subgraph = full_graph.create_complete_subgraph(
#         list(location.keys()))

#     # (currNode, currPath, currCost, currReward, visitedNodes)
#     queue = deque([(station,
#                     [starting_point, station.value],
#                     cost + location[station.value][1],
#                     location[station.value][0],
#                     set([station.value])) for station, cost in complete_subgraph.nodes[starting_point].edges])

#     currBestPath = []
#     currMaxReward = -1

#     while queue:
#         value = queue.popleft()
#         print(value)
#         currNode, currPath, currCost, currReward, visitedNodes = value
#         if currCost > time_limit:
#             continue
#         if currNode.value == starting_point:
#             if currReward > currMaxReward:
#                 currBestPath = currPath
#                 currMaxReward = currReward
#             continue
#         for nextNode, weight in currNode.edges:
#             if nextNode.value not in visitedNodes:
#                 queue.append((nextNode,
#                               currPath + [nextNode.value],
#                               currCost + location[nextNode.value][1] + weight,
#                               currReward + location[nextNode.value][0],
#                               visitedNodes.union({nextNode.value})))

#     return currBestPath, currMaxReward


# if __name__ == "__main__":
#     bestPath, maxReward = tourist(TEST_INPUT_2)
#     # print(f"input: {TEST_INPUT2}")
#     print(f"bestPath: {bestPath}")
#     print(f"maxReward: {maxReward}")
#     return_dict = {'path': currBestPath, 'satisfaction': currMaxReward}
#     logging.info("My result :{}".format(return_dict))
#     return json.dumps(return_dict)