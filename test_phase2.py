import csv
from pathlib import Path

from src.models import parcel_from_row
from src.sorting import merge_sort
from src.knapsack import knapsack


# Project directory
BASE_DIR = Path(__file__).resolve().parent
PARCEL_FILE = BASE_DIR / "datasets" / "parcels.csv"

# Vehicle capacity
VEHICLE_CAPACITY = 15


# Step 1: Read parcel dataset
with open(PARCEL_FILE, "r", encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))

parcels = [parcel_from_row(row) for row in rows]


# Step 2: Sort parcels using Merge Sort
sorted_parcels = merge_sort(parcels)

print("=" * 55)
print("       PHASE 2: PARCEL PRIORITIZATION")
print("=" * 55)

print("\nSORTED PARCELS (MERGE SORT)")
print("-" * 55)

for parcel in sorted_parcels:
    print(
        parcel.parcel_id,
        "| Priority:", parcel.priority,
        "| Deadline:", parcel.deadline,
        "| Weight:", parcel.weight, "kg",
        "| Value:", parcel.value
    )


# Step 3: Apply 0/1 Knapsack
selected, dp = knapsack(
    sorted_parcels,
    VEHICLE_CAPACITY
)


# Step 4: Display selected parcels
print("\nOPTIMAL PACKING PLAN")
print("-" * 55)

total_weight = sum(p.weight for p in selected)
total_value = sum(p.value for p in selected)

for parcel in selected:
    print(
        parcel.parcel_id,
        "| Weight:", parcel.weight, "kg",
        "| Value:", parcel.value
    )

print("\nVehicle Capacity:", VEHICLE_CAPACITY, "kg")
print("Total Selected Weight:", total_weight, "kg")
print("Remaining Capacity:", VEHICLE_CAPACITY - total_weight, "kg")
print("Maximum Total Value:", total_value)


# Step 5: Display complete DP table
print("\nDYNAMIC PROGRAMMING TABLE")
print("-" * 55)

header = "Parcel".ljust(10)

for capacity in range(VEHICLE_CAPACITY + 1):
    header += str(capacity).rjust(4)

print(header)

for i, row in enumerate(dp):
    if i == 0:
        label = "None"
    else:
        label = sorted_parcels[i - 1].parcel_id

    line = label.ljust(10)

    for value in row:
        line += str(value).rjust(4)

    print(line)


print("\nPhase 2 completed successfully!")
