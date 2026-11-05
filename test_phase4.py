import csv
import importlib
from pathlib import Path

try:
    plt = importlib.import_module("matplotlib.pyplot")
except ModuleNotFoundError:
    plt = None

from src.benchmark import (
    benchmark_sorting,
    benchmark_knapsack,
    benchmark_dijkstra,
    benchmark_tsp
)


# Project folders
BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "images"

IMAGE_DIR.mkdir(exist_ok=True)


print("=" * 60)
print("       PHASE 4: PERFORMANCE TESTING")
print("=" * 60)


# -----------------------------------
# 1. Sorting benchmark
# -----------------------------------

print("\n1. SORTING PERFORMANCE")
print("-" * 60)

sorting_results = benchmark_sorting(
    [100, 500, 1000, 2000]
)

for result in sorting_results:
    print(
        result["algorithm"],
        "| Input:", result["input_size"],
        "| Runtime:", round(result["runtime"], 6), "seconds"
    )


# -----------------------------------
# 2. Knapsack benchmark
# -----------------------------------

print("\n2. KNAPSACK PERFORMANCE")
print("-" * 60)

knapsack_results = benchmark_knapsack([
    (20, 50),
    (40, 100),
    (60, 150),
    (100, 200)
])

for result in knapsack_results:
    print(
        result["algorithm"],
        "| Parcels:", result["input_size"],
        "| Capacity:", result["capacity"],
        "| Runtime:", round(result["runtime"], 6), "seconds"
    )


# -----------------------------------
# 3. Dijkstra benchmark
# -----------------------------------

print("\n3. DIJKSTRA PERFORMANCE")
print("-" * 60)

dijkstra_results = benchmark_dijkstra(
    [10, 30, 50, 100]
)

for result in dijkstra_results:
    print(
        result["algorithm"],
        "| Nodes:", result["input_size"],
        "| Runtime:", round(result["runtime"], 6), "seconds"
    )


# -----------------------------------
# 4. TSP benchmark
# -----------------------------------

print("\n4. TSP PERFORMANCE")
print("-" * 60)

tsp_results = benchmark_tsp(
    [5, 10, 20, 30]
)

for result in tsp_results:
    print(
        result["algorithm"],
        "| Nodes:", result["input_size"],
        "| Runtime:", round(result["runtime"], 6), "seconds"
    )


# -----------------------------------
# 5. Save all benchmark results
# -----------------------------------

all_results = (
    sorting_results
    + knapsack_results
    + dijkstra_results
    + tsp_results
)

csv_file = IMAGE_DIR / "runtime_results.csv"

with csv_file.open(
    "w", newline="", encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "algorithm",
            "input_size",
            "capacity",
            "runtime"
        ],
        extrasaction="ignore"
    )

    writer.writeheader()

    for result in all_results:
        writer.writerow(result)


# -----------------------------------
# 6. Helper function for charts
# -----------------------------------

def save_chart(results, title, filename, series_names=None):

    if plt is None:
        print(f"Skipping chart '{filename}': matplotlib is not installed.")
        return

    plt.figure(figsize=(9, 5))

    algorithms = series_names or list({
        result["algorithm"] for result in results
    })

    for algorithm in algorithms:

        selected = [
            result for result in results
            if result["algorithm"] == algorithm
        ]

        selected.sort(key=lambda item: item["input_size"])

        x = [item["input_size"] for item in selected]
        y = [item["runtime"] for item in selected]

        plt.plot(
            x, y,
            marker="o",
            label=algorithm
        )

    plt.title(title)
    plt.xlabel("Input Size")
    plt.ylabel("Execution Time (seconds)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(IMAGE_DIR / filename, dpi=300)
    plt.close()


# -----------------------------------
# 7. Generate performance charts
# -----------------------------------

save_chart(
    sorting_results,
    "Sorting Algorithm Performance",
    "sorting_performance.png",
    ["Merge Sort", "Python Built-in Sort"]
)

save_chart(
    knapsack_results,
    "0/1 Knapsack Performance",
    "knapsack_performance.png"
)

save_chart(
    dijkstra_results,
    "Dijkstra Algorithm Performance",
    "dijkstra_performance.png"
)

save_chart(
    tsp_results,
    "Nearest Neighbor TSP Performance",
    "tsp_performance.png"
)


print("\n" + "=" * 60)
print("BENCHMARKING COMPLETED")
print("=" * 60)

print("\nRuntime data saved at:")
print(csv_file)

print("\nCharts generated:")
print("1. sorting_performance.png")
print("2. knapsack_performance.png")
print("3. dijkstra_performance.png")
print("4. tsp_performance.png")

print("\nPhase 4 completed successfully!")
