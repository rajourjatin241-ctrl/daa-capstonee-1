import csv
from pathlib import Path

from src.models import parcel_from_row

BASE_DIR = Path(__file__).resolve().parent

PARCEL_FILE = BASE_DIR / "datasets" / "parcels.csv"
ROAD_FILE = BASE_DIR / "datasets" / "roads.csv"


with open(PARCEL_FILE, "r", encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))

parcels = [parcel_from_row(row) for row in rows]


with open(ROAD_FILE, "r", encoding="utf-8-sig", newline="") as file:
    roads = list(csv.DictReader(file))

print("=" * 40)
print("       MINI-COURIER PLANNER")
print("=" * 40)

print("\nPARCEL INFORMATION")
print("-" * 40)
print("Total parcels:", len(parcels))

for parcel in parcels:
    print(
        parcel.parcel_id,
        "| Destination:", parcel.destination,
        "| Weight:", parcel.weight, "kg",
        "| Priority:", parcel.priority,
        "| Value:", parcel.value
    )

print("\nROAD NETWORK INFORMATION")
print("-" * 40)
print("Total road connections:", len(roads))

for road in roads:
    print(
        road["source"],
        "<->",
        road["destination"],
        "| Distance:", road["distance"], "km"
    )

print("\nPhase 1 completed successfully!")
