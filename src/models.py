
from dataclasses import dataclass


@dataclass
class Parcel:
    parcel_id: str
    destination: str
    weight: int
    priority: int
    deadline: int
    value: int


def parcel_from_row(row):
    """Convert one CSV row into a Parcel object."""
    return Parcel(
        parcel_id=row["parcel_id"],
        destination=row["destination"],
        weight=int(row["weight"]),
        priority=int(row["priority"]),
        deadline=int(row["deadline"]),
        value=int(row["value"]),
    )
