from datetime import datetime

from sqlmodel import Field, SQLModel


class Trip(SQLModel, table=True):
    """
    SQLModel representing a taxi trip record.

    This model maps to the 'trips' table in the database.
    """

    __tablename__: str = "trips"

    id: str = Field(primary_key=True, description="Unique identifier for the trip")
    vendor_id: int = Field(description="Vendor/provider ID")
    pickup_datetime: datetime = Field(
        description="Timestamp when the passenger was picked up"
    )
    dropoff_datetime: datetime = Field(
        description="Timestamp when the passenger was dropped off"
    )
    passenger_count: int = Field(description="Number of passengers in the trip")
    pickup_longitude: float = Field(
        description="Longitude coordinate of pickup location"
    )
    pickup_latitude: float = Field(description="Latitude coordinate of pickup location")
    dropoff_longitude: float = Field(
        description="Longitude coordinate of dropoff location"
    )
    dropoff_latitude: float = Field(
        description="Latitude coordinate of dropoff location"
    )
    store_and_fwd_flag: str = Field(
        description="Flag indicating if trip record was held in vehicle memory before sending to vendor"
    )
    trip_duration: int = Field(description="Duration of the trip in seconds")