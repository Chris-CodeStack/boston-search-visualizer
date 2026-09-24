# test_algos.py
import json
from uninformed import (
    breadth_first_search,
    depth_first_search,
    uniform_cost_search,
    iterative_deepening_search,
)
from informed import (
    a_star_search,
    greedy_best_first_search,
    sma_star_search,
)

# 1. Load map data
with open("map_data.json", "r") as f:
    data = json.load(f)

graph = data["graph"]
locations = data["locations"]

start_city = "Boston, MA"
goal_city = "Dedham, MA"

print(f"Testing search from '{start_city}' to '{goal_city}'...\n")

algorithms = {
    "BFS": lambda: breadth_first_search(graph, start_city, goal_city),
    "DFS": lambda: depth_first_search(graph, start_city, goal_city),
    "UCS": lambda: uniform_cost_search(graph, start_city, goal_city),
    "IDS": lambda: iterative_deepening_search(graph, start_city, goal_city),
    "Greedy": lambda: greedy_best_first_search(graph, start_city, goal_city, locations),
    "A*": lambda: a_star_search(graph, start_city, goal_city, locations),
    "SMA*": lambda: sma_star_search(graph, start_city, goal_city, locations, memory_limit=15),
}

for name, algo_func in algorithms.items():
    try:
        res = algo_func()
        path = res.get("path", [])
        cost = res.get("cost", 0.0)
        expanded = res.get("nodes_expanded", 0)
        
        status = "PASSED" if len(path) > 0 and path[0] == start_city and path[-1] == goal_city else "FAILED"
        print(f"[{status}] {name:8s} | Cost: {cost:6.2f} mi | Expanded: {expanded:2d} nodes | Steps: {len(path)}")
    except Exception as e:
        print(f"[ERROR]  {name:8s} | Threw exception: {e}")