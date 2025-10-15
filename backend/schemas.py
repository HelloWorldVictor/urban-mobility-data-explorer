"""Query schemas for filtering and sorting trips data."""

from enum import Enum


class SortOrder(str, Enum):
    """Sort order options."""

    asc = "asc"
    desc = "desc"


class SortField(Enum):
    """Available fields for sorting."""

    pickup_datetime = "pickup_datetime"
    dropoff_datetime = "dropoff_datetime"
    trip_duration = "trip_duration"
    passenger_count = "passenger_count"
    vendor_id = "vendor_id"
