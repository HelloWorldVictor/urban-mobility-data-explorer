"""Analytics and aggregation response models."""

from datetime import datetime

from pydantic import BaseModel, Field


class TripStats(BaseModel):
    """Statistical summary of trips."""

    total_trips: int = Field(description="Total number of trips")
    total_duration: float = Field(description="Average trip duration in seconds")
    total_passengers: int = Field(description="Total number of passengers transported")


class TimeSeriesPoint(BaseModel):
    """Single point in time series."""

    timestamp: datetime = Field(description="Timestamp")
    trip_count: int = Field(description="Number of trips")
    avg_duration: float = Field(description="Average duration in seconds")
