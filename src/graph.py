import heapq


def build_graph(roads):
    """
    Create an undirected weighted graph
    using the roads dataset.
    """

    graph = {}

    for road in roads:
        source = road["source"].strip()
        destination = road["destination"].strip()
        distance = float(road["distance"])

        # Create nodes if they don't exist
        if source not in graph:
            graph[source] = {}

        if destination not in graph:
            graph[destination] = {}

        # Add bidirectional roads
        graph[source][destination] = distance
        graph[destination][source] = distance

    return graph


def dijkstra(graph, start, end):
    """
    Find the shortest path between two locations
    using Dijkstra's Algorithm.

    Returns:
        shortest_distance
        shortest_path
    """

    distances = {
        node: float("inf") for node in graph
    }

    previous = {
        node: None for node in graph
    }

    distances[start] = 0

    # Priority queue: (distance, node)
    priority_queue = [(0, start)]

    while priority_queue:

        current_distance, current_node = heapq.heappop(
            priority_queue
        )

        # Ignore outdated entries
        if current_distance > distances[current_node]:
            continue

        if current_node == end:
            break

        # Explore neighboring locations
        for neighbor, weight in graph[current_node].items():

            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:

                distances[neighbor] = new_distance

                previous[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    # Check if destination is reachable
    if distances[end] == float("inf"):
        return float("inf"), []

    # Reconstruct shortest path
    path = []
    current = end

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    return distances[end], path
