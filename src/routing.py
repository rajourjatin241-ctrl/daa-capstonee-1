from src.graph import dijkstra


def nearest_neighbor_tsp(graph, start, destinations):
    """
    Create a delivery route using the
    Nearest-Neighbor TSP approximation.

    Starts at the depot, visits every unique
    destination, and returns to the depot.
    """

    # Remove duplicate destinations and the depot
    remaining = sorted(
        set(destinations) - {start}
    )

    current = start

    route = [start]
    complete_path = [start]
    total_distance = 0

    # Visit nearest unvisited destination
    while remaining:

        nearest_location = None
        shortest_distance = float("inf")
        shortest_path = []

        for destination in remaining:

            distance, path = dijkstra(
                graph, current, destination
            )

            if distance < shortest_distance:
                shortest_distance = distance
                nearest_location = destination
                shortest_path = path

        if nearest_location is None or not shortest_path:
            raise ValueError(
                "Some delivery locations are unreachable."
            )

        total_distance += shortest_distance

        route.append(nearest_location)

        # Add actual road path without repeating
        # the current location
        complete_path.extend(shortest_path[1:])

        current = nearest_location

        remaining.remove(nearest_location)

    # Return to depot
    return_distance, return_path = dijkstra(
        graph, current, start
    )

    if not return_path:
        raise ValueError("Depot cannot be reached.")

    total_distance += return_distance

    route.append(start)

    complete_path.extend(return_path[1:])

    return route, complete_path, total_distance
