import json
import os
from flask import Flask, jsonify, render_template, request

from uninformed import (
    breadth_first_search,
    depth_first_search,
    iterative_deepening_search,
    uniform_cost_search,
)
from informed import (
    a_star_search,
    greedy_best_first_search,
)

app = Flask(__name__)

MAP_DATA_FILE = "map_data.json"

def load_map_data():
    if os.path.exists(MAP_DATA_FILE):
        try:
            with open(MAP_DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {MAP_DATA_FILE}: {e}")

    return {
        "region": "Greater Boston, MA, USA",
        "total_cities": 0,
        "total_edges": 0,
        "locations": {},
        "graph": {}
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/map", methods=["GET"])
def get_map():
    data = load_map_data()
    return jsonify(data)

@app.route("/api/search", methods=["POST"])
def search():
    payload = request.get_json() or {}
    start = payload.get("start", "").strip()
    goal = payload.get("goal", "").strip()
    algorithm = payload.get("algorithm", "bfs").strip().lower()

    map_data = load_map_data()
    graph = map_data.get("graph", {})
    locations = map_data.get("locations", {})

    if not start or not goal:
        return jsonify({"error": "Start and goal cities must be provided."}), 400

    if start not in graph or goal not in graph:
        return jsonify({"error": f"Invalid start or goal node: '{start}' or '{goal}'."}), 400

    if algorithm == "bfs":
        result = breadth_first_search(graph, start, goal)
    elif algorithm == "dfs":
        result = depth_first_search(graph, start, goal)
    elif algorithm == "ucs":
        result = uniform_cost_search(graph, start, goal)
    elif algorithm == "ids":
        result = iterative_deepening_search(graph, start, goal)
    elif algorithm == "greedy":
        result = greedy_best_first_search(graph, start, goal, locations)
    elif algorithm == "astar":
        result = a_star_search(graph, start, goal, locations)
    else:
        return jsonify({"error": f"Unsupported algorithm '{algorithm}'."}), 400

    return jsonify({
        "status": "success",
        "algorithm": algorithm,
        "start": start,
        "goal": goal,
        "path": result.get("path", []),
        "cost": result.get("cost", 0.0),
        "visited_order": result.get("visited_order", []),
        "nodes_expanded": result.get("nodes_expanded", len(result.get("visited_order", [])))
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)