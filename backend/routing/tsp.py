import numpy as np

def calculate_optimal_route(incidents, start_point=None):
    """
    Given a list of incidents, calculates a TSP route.
    For simplicity in this MVP, we use straight-line distance.
    In production, this would query an OSM routing engine (like OSRM) for real street distances.
    """
    if not incidents or len(incidents) < 2:
        return [i.id for i in incidents]

    points = []
    if start_point:
        points.append((start_point.y, start_point.x)) # [lat, lon]

    for inc in incidents:
        points.append((inc.center_location.y, inc.center_location.x))

    n = len(points)
    dist_matrix = np.zeros((n, n))

    # Simple Euclidean distance matrix (could be replaced with Haversine)
    for i in range(n):
        for j in range(n):
            if i != j:
                dist_matrix[i][j] = np.linalg.norm(np.array(points[i]) - np.array(points[j]))

    # We use a greedy/simulated annealing TSP solver from python-tsp
    # But since we didn't install python-tsp, we'll write a simple nearest-neighbor heuristic

    unvisited = list(range(n))
    current = unvisited.pop(0) # Start at index 0
    route_indices = [current]

    while unvisited:
        nearest = min(unvisited, key=lambda x: dist_matrix[current][x])
        route_indices.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    # Map back to incident IDs
    route_incident_ids = []

    offset = 1 if start_point else 0

    for idx in route_indices:
        if start_point and idx == 0:
            continue
        route_incident_ids.append(incidents[idx - offset].id)

    return route_incident_ids
