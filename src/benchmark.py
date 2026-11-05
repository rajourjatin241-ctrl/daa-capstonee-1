import random
import time
import statistics

from src.models import Parcel
from src.sorting import merge_sort
from src.knapsack import knapsack
from src.graph import build_graph, dijkstra
from src.routing import nearest_neighbor_tsp


# Make experiments reproducible
random.seed(42)


def measure_runtime(function, repeats=5):
    """
    Execute a function multiple times
    and return its median execution time.
    """

    times = []

    for _ in range(repeats):

        start = time.perf_counter()

        function()

        end = time.perf_counter()

        times.append(end - start)

    return statistics.median(times)


# -----------------------------------
# 1. Generate random parcel datasets
# -----------------------------------

def generate_parcels(number):
    """Generate random parcels for benchmarking."""

    parcels = []

    for i in range(number):

        parcel = Parcel(
            parcel_id=f"P{i + 1}",
            destination=f"D{i % 20 + 1}",
            weight=random.randint(1, 10),
            priority=random.randint(1, 5),
            deadline=random.randint(1, 30),
            value=random.randint(20, 150)
        )

        parcels.append(parcel)

    return parcels


# -----------------------------------
# 2. Generate a connected road graph
# -----------------------------------

def generate_graph(number):
    """
    Generate a connected undirected weighted graph.
    A chain guarantees that every node is reachable.
    Additional edges create alternative routes.
    """

    roads = []

    # Connect consecutive nodes
    for i in range(number - 1):

        roads.append({
            "source": f"N{i}",
            "destination": f"N{i + 1}",
            "distance": random.randint(1, 20)
        })

    # Add extra random connections
    for _ in range(number * 2):

        source = random.randint(0, number - 1)
        destination = random.randint(0, number - 1)

        if source != destination:

            roads.append({
                "source": f"N{source}",
                "destination": f"N{destination}",
                "distance": random.randint(1, 20)
            })

    return build_graph(roads)


# -----------------------------------
# 3. Benchmark sorting algorithms
# -----------------------------------

def benchmark_sorting(sizes):

    results = []

    for size in sizes:

        parcels = generate_parcels(size)

        merge_time = measure_runtime(
            lambda: merge_sort(parcels)
        )

        builtin_time = measure_runtime(
            lambda: sorted(
                parcels,
                key=lambda p: (p.priority, p.deadline)
            )
        )

        results.append({
            "algorithm": "Merge Sort",
            "input_size": size,
            "runtime": merge_time
        })

        results.append({
            "algorithm": "Python Built-in Sort",
            "input_size": size,
            "runtime": builtin_time
        })

    return results


# -----------------------------------
# 4. Benchmark Knapsack algorithm
# -----------------------------------

def benchmark_knapsack(configurations):

    results = []

    for number, capacity in configurations:

        parcels = generate_parcels(number)

        runtime = measure_runtime(
            lambda: knapsack(parcels, capacity)
        )

        results.append({
            "algorithm": "0/1 Knapsack",
            "input_size": number,
            "capacity": capacity,
            "runtime": runtime
        })

    return results


# -----------------------------------
# 5. Benchmark Dijkstra algorithm
# -----------------------------------

def benchmark_dijkstra(sizes):

    results = []

    for size in sizes:

        graph = generate_graph(size)

        start_node = "N0"
        end_node = f"N{size - 1}"

        runtime = measure_runtime(
            lambda: dijkstra(graph, start_node, end_node)
        )

        results.append({
            "algorithm": "Dijkstra",
            "input_size": size,
            "runtime": runtime
        })

    return results


# -----------------------------------
# 6. Benchmark TSP algorithm
# -----------------------------------

def benchmark_tsp(sizes):

    results = []

    for size in sizes:

        graph = generate_graph(size)

        destinations = [
            f"N{i}" for i in range(1, size)
        ]

        runtime = measure_runtime(
            lambda: nearest_neighbor_tsp(
                graph, "N0", destinations
            )
        )

        results.append({
            "algorithm": "Nearest Neighbor TSP",
            "input_size": size,
            "runtime": runtime
        })

    return results
