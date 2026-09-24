"""
informed.py
===========
Implementation of informed (heuristic) search algorithms:
  - Straight-Line Haversine Heuristic h(n)
  - Greedy Best-First Search
  - A* Search
"""

import math
import heapq


def haversine_heuristic(node, goal, locations):
    if node not in locations or goal not in locations:
        return 0.0

    lat1, lon1 = locations[node]["lat"], locations[node]["lon"]
    lat2, lon2 = locations[goal]["lat"], locations[goal]["lon"]
    r_earth = 3958.8  # Earth radius in miles

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(r_earth * c, 2)


def compute_path_cost(graph, path):
    if not path or len(path) < 2:
        return 0.0
    return round(sum(graph[path[i]][path[i + 1]] for i in range(len(path) - 1)), 2)


def greedy_best_first_search(graph, start, goal, locations):
    counter = 0
    h_start = haversine_heuristic(start, goal, locations)
    pq = [(h_start, counter, start, [start])]
    visited = set()
    visited_order = []

    while pq:
        h_val, _, current, path = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)
        visited_order.append(current)

        if current == goal:
            return {
                "path": path,
                "cost": compute_path_cost(graph, path),
                "visited_order": visited_order,
                "nodes_expanded": len(visited_order)
            }

        for neighbor in sorted(graph.get(current, {}).keys()):
            if neighbor not in visited:
                counter += 1
                h_next = haversine_heuristic(neighbor, goal, locations)
                heapq.heappush(pq, (h_next, counter, neighbor, path + [neighbor]))

    return {"path": [], "cost": 0.0, "visited_order": visited_order, "nodes_expanded": len(visited_order)}


def a_star_search(graph, start, goal, locations):
    """
    A* Search
    Minimizes f(n) = g(n) + h(n).
    Guarantees an optimal path when h(n) is admissible (Haversine straight-line distance).
    """
    counter = 0
    h_start = haversine_heuristic(start, goal, locations)
    pq = [(h_start, counter, 0.0, start, [start])]
    visited_order = []
    g_costs = {start: 0.0}
    closed_set = set()

    while pq:
        f_val, _, g_val, current, path = heapq.heappop(pq)

        if current in closed_set:
            continue
        closed_set.add(current)
        visited_order.append(current)

        if current == goal:
            return {
                "path": path,
                "cost": round(g_val, 2),
                "visited_order": visited_order,
                "nodes_expanded": len(visited_order)
            }

        for neighbor, edge_weight in sorted(graph.get(current, {}).items()):
            tentative_g = g_val + edge_weight
            if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                g_costs[neighbor] = tentative_g
                h_neighbor = haversine_heuristic(neighbor, goal, locations)
                f_neighbor = tentative_g + h_neighbor
                counter += 1
                heapq.heappush(pq, (f_neighbor, counter, tentative_g, neighbor, path + [neighbor]))

    return {"path": [], "cost": 0.0, "visited_order": visited_order, "nodes_expanded": len(visited_order)}