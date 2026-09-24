from collections import deque
import heapq


def compute_path_cost(graph, path):
    if not path or len(path) < 2:
        return 0.0
    return round(sum(graph[path[i]][path[i + 1]] for i in range(len(path) - 1)), 2)

def breadth_first_search(graph, start, goal):
    if start == goal:
        return {"path": [start], "cost": 0.0, "visited_order": [start], "nodes_expanded": 1}

    queue = deque([[start]])
    visited = {start}
    visited_order = []

    while queue:
        path = queue.popleft()
        current = path[-1]
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
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return {"path": [], "cost": 0.0, "visited_order": visited_order, "nodes_expanded": len(visited_order)}

def depth_first_search(graph, start, goal):
    if start == goal:
        return {"path": [start], "cost": 0.0, "visited_order": [start], "nodes_expanded": 1}

    stack = [[start]]
    visited = set()
    visited_order = []

    while stack:
        path = stack.pop()
        current = path[-1]

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

        for neighbor in sorted(graph.get(current, {}).keys(), reverse=True):
            if neighbor not in visited:
                stack.append(path + [neighbor])

    return {"path": [], "cost": 0.0, "visited_order": visited_order, "nodes_expanded": len(visited_order)}

def uniform_cost_search(graph, start, goal):
    """
    Uniform-Cost Search (UCS)
    Expands lowest path-cost (g) node first using a min-priority queue.
    Guarantees the optimal road-distance path on positive edge costs.
    """
    counter = 0
    pq = [(0.0, counter, start, [start])]
    visited_order = []
    min_cost = {start: 0.0}

    while pq:
        cost, _, current, path = heapq.heappop(pq)

        if current in visited_order:
            continue
        visited_order.append(current)

        if current == goal:
            return {
                "path": path,
                "cost": round(cost, 2),
                "visited_order": visited_order,
                "nodes_expanded": len(visited_order)
            }

        for neighbor, edge_weight in sorted(graph.get(current, {}).items()):
            new_cost = cost + edge_weight
            if neighbor not in min_cost or new_cost < min_cost[neighbor]:
                min_cost[neighbor] = new_cost
                counter += 1
                heapq.heappush(pq, (new_cost, counter, neighbor, path + [neighbor]))

    return {"path": [], "cost": 0.0, "visited_order": visited_order, "nodes_expanded": len(visited_order)}

def iterative_deepening_search(graph, start, goal, max_depth=50):
    """
    Iterative Deepening Search (IDS)
    Combines DFS space efficiency with BFS level-by-level completeness.
    """
    visited_order = []

    def dls(path, depth):
        current = path[-1]
        visited_order.append(current)

        if current == goal:
            return path
        if depth <= 0:
            return None

        for neighbor in sorted(graph.get(current, {}).keys()):
            if neighbor not in path: 
                result = dls(path + [neighbor], depth - 1)
                if result is not None:
                    return result
        return None

    for depth_limit in range(max_depth):
        found_path = dls([start], depth_limit)
        if found_path:
            return {
                "path": found_path,
                "cost": compute_path_cost(graph, found_path),
                "visited_order": visited_order,
                "nodes_expanded": len(visited_order)
            }

    return {"path": [], "cost": 0.0, "visited_order": visited_order, "nodes_expanded": len(visited_order)}