import csv
from pathlib import Path

from src.models import parcel_from_row
from src.knapsack import knapsack
from src.sorting import merge_sort
from src.graph import build_graph, dijkstra
from src.routing import nearest_neighbor_tsp


# Project directory
BASE_DIR = Path(__file__).resolve().parent

PARCEL_FILE = BASE_DIR / "datasets" / "parcels.csv"
ROAD_FILE = BASE_DIR / "datasets" / "roads.csv"

VEHICLE_CAPACITY = 15
DEPOT = "DEPOT"


# STEP 1: Load parcels
with open(
    PARCEL_FILE, "r", encoding="utf-8-sig", newline=""
) as file:
    parcel_rows = list(csv.DictReader(file))

parcels = [
    parcel_from_row(row) for row in parcel_rows
]


# STEP 2: Sort and select parcels
sorted_parcels = merge_sort(parcels)

selected_parcels, dp = knapsack(
    sorted_parcels, VEHICLE_CAPACITY
)


# STEP 3: Extract unique destinations
destinations = sorted({
    parcel.destination for parcel in selected_parcels
})


# STEP 4: Load roads and build graph
with open(
    ROAD_FILE, "r", encoding="utf-8-sig", newline=""
) as file:
    road_rows = list(csv.DictReader(file))

graph = build_graph(road_rows)


print("=" * 55)
print("       PHASE 3: ROUTE MAKER")
print("=" * 55)


# STEP 5: Display graph
print("\nROAD NETWORK GRAPH")
print("-" * 55)

for location, neighbors in graph.items():
    print(location, "->", neighbors)


# STEP 6: Individual shortest paths
print("\nDIJKSTRA SHORTEST PATHS FROM DEPOT")
print("-" * 55)

for destination in destinations:

    distance, path = dijkstra(
        graph, DEPOT, destination
    )

    print(
        DEPOT, "to", destination,
        "| Path:", " -> ".join(path),
        "| Distance:", distance, "km"
    )


# STEP 7: Overall delivery route
route, complete_path, total_distance = (
    nearest_neighbor_tsp(
        graph, DEPOT, destinations
    )
)


# STEP 8: Display final results
print("\nSELECTED DELIVERY PARCELS")
print("-" * 55)

for parcel in selected_parcels:
    print(
        parcel.parcel_id,
        "| Destination:", parcel.destination,
        "| Weight:", parcel.weight, "kg"
    )


print("\nUNIQUE DELIVERY DESTINATIONS")
print("-" * 55)

print(destinations)


print("\nOPTIMIZED DELIVERY SEQUENCE")
print("-" * 55)

print(" -> ".join(route))


print("\nACTUAL ROAD-BY-ROAD PATH")
print("-" * 55)

print(" -> ".join(complete_path))


print("\nTOTAL DELIVERY DISTANCE")
print("-" * 55)

print(total_distance, "km")


print("\nPhase 3 completed successfully!")
