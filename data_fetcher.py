import json
import math
import time
import requests

REGION_NAME = "Greater Boston, MA, USA"

CITIES = [
    "Boston, MA",
    "Cambridge, MA",
    "Somerville, MA",
    "Brookline, MA",
    "Newton, MA",
    "Watertown, MA",
    "Waltham, MA",
    "Quincy, MA",
    "Medford, MA",
    "Malden, MA",
    "Revere, MA",
    "Chelsea, MA",
    "Arlington, MA",
    "Lexington, MA",
    "Woburn, MA",
    "Dedham, MA",
    "Braintree, MA",
    "Framingham, MA",
    "Natick, MA",
    "Concord, MA",
    "Burlington, MA",
    "Lynn, MA"
]

ROAD_CONNECTIONS = [
    ("Boston, MA", "Cambridge, MA"),
    ("Boston, MA", "Brookline, MA"),
    ("Boston, MA", "Chelsea, MA"),
    ("Boston, MA", "Quincy, MA"),
    ("Boston, MA", "Somerville, MA"),
    ("Cambridge, MA", "Somerville, MA"),
    ("Cambridge, MA", "Watertown, MA"),
    ("Somerville, MA", "Medford, MA"),
    ("Medford, MA", "Malden, MA"),
    ("Chelsea, MA", "Revere, MA"),
    ("Malden, MA", "Revere, MA"),
    ("Revere, MA", "Lynn, MA"),
    ("Malden, MA", "Melrose, MA" if "Melrose, MA" in CITIES else "Woburn, MA"),
    ("Brookline, MA", "Newton, MA"),
    ("Watertown, MA", "Newton, MA"),
    ("Watertown, MA", "Waltham, MA"),
    ("Newton, MA", "Waltham, MA"),
    ("Newton, MA", "Dedham, MA"),
    ("Cambridge, MA", "Arlington, MA"),
    ("Arlington, MA", "Medford, MA"),
    ("Arlington, MA", "Lexington, MA"),
    ("Lexington, MA", "Concord, MA"),
    ("Waltham, MA", "Lexington, MA"),
    ("Waltham, MA", "Concord, MA"),
    ("Medford, MA", "Woburn, MA"),
    ("Woburn, MA", "Burlington, MA"),
    ("Burlington, MA", "Lexington, MA"),
    ("Burlington, MA", "Woburn, MA"),
    ("Lynn, MA", "Malden, MA"),
    ("Newton, MA", "Natick, MA"),
    ("Natick, MA", "Framingham, MA"),
    ("Waltham, MA", "Natick, MA"),
    ("Framingham, MA", "Concord, MA"),
    ("Boston, MA", "Dedham, MA"),
    ("Dedham, MA", "Braintree, MA"),
    ("Quincy, MA", "Braintree, MA"),
    ("Brookline, MA", "Dedham, MA"),
    ("Natick, MA", "Dedham, MA")
]

USER_AGENT = "Boston-Map-Search-Visualizer/1.0 (academic-ai-project)"


def haversine_distance(coord1, coord2):
    """
    Fallback straight-line (great-circle) distance in miles.
    coord = (lat, lon)
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    r_earth = 3958.8

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(r_earth * c, 2)


def fetch_coordinates(city_name):
    """
    Fetch latitude and longitude from Nominatim OpenStreetMap API.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": USER_AGENT
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                return {"lat": lat, "lon": lon}
    except Exception as exc:
        print(f"  [Warning] Failed to fetch coordinates for {city_name}: {exc}")

    return None


def fetch_road_distance(coord1, coord2):
    """
    Fetch driving road distance in miles from OSRM Routing API.
    coord = (lat, lon)
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}"
    params = {"overview": "false"}

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "Ok" and len(data.get("routes", [])) > 0:
                distance_meters = data["routes"][0]["distance"]
                distance_miles = distance_meters * 0.000621371
                return round(distance_miles, 2)
    except Exception as exc:
        print(f"  [Warning] OSRM routing failed ({coord1} -> {coord2}): {exc}")

    return haversine_distance(coord1, coord2)


def build_graph():
    """
    Build the map graph and save to map_data.json.
    """
    print(f"Building map graph for region: {REGION_NAME}")
    print(f"Total locations to geocode: {len(CITIES)}")

    locations = {}
    for idx, city in enumerate(CITIES, 1):
        print(f"[{idx}/{len(CITIES)}] Geocoding: {city} ...")
        coords = fetch_coordinates(city)
        if coords:
            locations[city] = coords
        else:
            print(f"  [Error] Could not find coordinates for {city}")
        # This is to comply with Nominatim usage policy (1 request/second)
        time.sleep(1.0)

    graph = {city: {} for city in locations}

    unique_edges = list({tuple(sorted([u, v])): (u, v) for u, v in ROAD_CONNECTIONS}.values())

    print(f"\nFetching road distances for {len(unique_edges)} connections ...")
    total_edges = 0
    for u, v in unique_edges:
        if u in locations and v in locations:
            c1 = (locations[u]["lat"], locations[u]["lon"])
            c2 = (locations[v]["lat"], locations[v]["lon"])
            dist = fetch_road_distance(c1, c2)

            graph[u][v] = dist
            graph[v][u] = dist
            total_edges += 1
            print(f"  Connection: {u} <---> {v} : {dist} miles")
            time.sleep(0.2)
        else:
            print(f"  [Warning] Skipping edge ({u}, {v}) - missing coordinates.")

    map_data = {
        "region": REGION_NAME,
        "total_cities": len(locations),
        "total_edges": total_edges,
        "locations": locations,
        "graph": graph
    }

    with open("map_data.json", "w", encoding="utf-8") as f:
        json.dump(map_data, f, indent=2)

    print("\nGraph construction complete!")
    print(f"Saved to map_data.json with {len(locations)} cities and {total_edges} bidirectional connections.")


if __name__ == "__main__":
    build_graph()