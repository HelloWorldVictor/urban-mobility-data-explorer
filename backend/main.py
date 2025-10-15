from datetime import datetime
from typing import Any, Optional
from enum import Enum

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scalar_fastapi import Theme, get_scalar_api_reference
from sqlmodel import Session, col, func, select

from backend.analytics_models import TimeSeriesPoint, TripStats
from data.database import get_session
from backend.schemas import SortField, SortOrder
from data.models import Trip

# region setup
app = FastAPI(
    title="Urban Mobility Data Explorer API",
    description="API for exploring and analyzing taxi trip data with comprehensive filtering, sorting, and analytics",
    version="1.0.0",
)


# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    """Scalar API documentation."""
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        scalar_proxy_url="https://proxy.scalar.com",
        theme=Theme.KEPLER,
    )


class BaseResponse(BaseModel):
    message: str
    success: bool
    data: Any


# endregion


# region "/"
class HomeData(BaseModel):
    documentation: str
    endpoints: dict[str, str]


class HomeResponse(BaseResponse):
    message: str
    data: HomeData


@app.get("/", response_model=HomeResponse)
async def read_root() -> HomeResponse:
    """Root endpoint with API information."""
    return HomeResponse(
        message="Urban Mobility Data Explorer API",
        success=True,
        data=HomeData(
            documentation="/scalar",
            endpoints={
                "trips": "/api/trips - Get trips with filtering and sorting",
                "trip_by_id": "/api/trips/{trip_id} - Get specific trip",
                "statistics": "/api/analytics/stats - Overall statistics",
                "time_series": "/api/analytics/time-series - Time series data",
                "geospatial": "/api/analytics/geospatial - Location hotspots",
            },
        ),
    )


# endregion


# region "/trips"
class PaginationMeta(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class TripsResponse(BaseResponse):
    data: list[Trip]
    pagination: PaginationMeta


@app.get("/api/trips")
async def get_trips(
    pickup_start: Optional[datetime] = Query(
        None, description="Filter trips picked up after this time"
    ),
    pickup_end: Optional[datetime] = Query(
        None, description="Filter trips picked up before this time"
    ),
    dropoff_start: Optional[datetime] = Query(
        None, description="Filter trips dropped off after this time"
    ),
    dropoff_end: Optional[datetime] = Query(
        None, description="Filter trips dropped off before this time"
    ),
    min_duration: Optional[int] = Query(
        None, description="Minimum trip duration in seconds", ge=0
    ),
    max_duration: Optional[int] = Query(
        None, description="Maximum trip duration in seconds", ge=0
    ),
    min_passengers: Optional[int] = Query(
        None, description="Minimum number of passengers", ge=0
    ),
    max_passengers: Optional[int] = Query(
        None, description="Maximum number of passengers", ge=0
    ),
    vendor_id: Optional[int] = Query(None, description="Filter by vendor ID"),
    pickup_lat_min: Optional[float] = Query(
        None, description="Minimum pickup latitude"
    ),
    pickup_lat_max: Optional[float] = Query(
        None, description="Maximum pickup latitude"
    ),
    pickup_lon_min: Optional[float] = Query(
        None, description="Minimum pickup longitude"
    ),
    pickup_lon_max: Optional[float] = Query(
        None, description="Maximum pickup longitude"
    ),
    dropoff_lat_min: Optional[float] = Query(
        None, description="Minimum dropoff latitude"
    ),
    dropoff_lat_max: Optional[float] = Query(
        None, description="Maximum dropoff latitude"
    ),
    dropoff_lon_min: Optional[float] = Query(
        None, description="Minimum dropoff longitude"
    ),
    dropoff_lon_max: Optional[float] = Query(
        None, description="Maximum dropoff longitude"
    ),
    store_and_fwd_flag: Optional[str] = Query(
        None, description="Filter by store and forward flag (Y/N)"
    ),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        20, ge=1, le=1000, description="Maximum number of records to return"
    ),
    sort_by: SortField = Query(
        SortField.pickup_datetime, description="Field to sort by"
    ),
    sort_order=Query(SortOrder.desc, description="Sort order (asc/desc)"),
    session: Session = Depends(get_session),
) -> TripsResponse:
    """
    Get trips with comprehensive filtering and sorting options.

    Features:
    - Time-based filtering (pickup/dropoff times)
    - Duration filtering
    - Passenger count filtering
    - Vendor filtering
    - Geospatial filtering (bounding boxes)
    - Store and forward flag filtering
    - Pagination (skip/limit) with metadata
    - Sorting by multiple fields

    Returns pagination metadata including:
    - Total count of matching trips
    - Current page number
    - Total pages available
    - Has next/previous page flags
    """
    # Build base query for counting
    count_query = select(func.count(col(Trip.id)))
    data_query = select(Trip)

    # Apply filters to both queries
    filters = []
    if pickup_start:
        filters.append(Trip.pickup_datetime >= pickup_start)
    if pickup_end:
        filters.append(Trip.pickup_datetime <= pickup_end)
    if dropoff_start:
        filters.append(Trip.dropoff_datetime >= dropoff_start)
    if dropoff_end:
        filters.append(Trip.dropoff_datetime <= dropoff_end)
    if min_duration:
        filters.append(Trip.trip_duration >= min_duration)
    if max_duration:
        filters.append(Trip.trip_duration <= max_duration)
    if min_passengers:
        filters.append(Trip.passenger_count >= min_passengers)
    if max_passengers:
        filters.append(Trip.passenger_count <= max_passengers)
    if vendor_id:
        filters.append(Trip.vendor_id == vendor_id)
    if pickup_lat_min:
        filters.append(Trip.pickup_latitude >= pickup_lat_min)
    if pickup_lat_max:
        filters.append(Trip.pickup_latitude <= pickup_lat_max)
    if pickup_lon_min:
        filters.append(Trip.pickup_longitude >= pickup_lon_min)
    if pickup_lon_max:
        filters.append(Trip.pickup_longitude <= pickup_lon_max)
    if dropoff_lat_min:
        filters.append(Trip.dropoff_latitude >= dropoff_lat_min)
    if dropoff_lat_max:
        filters.append(Trip.dropoff_latitude <= dropoff_lat_max)
    if dropoff_lon_min:
        filters.append(Trip.dropoff_longitude >= dropoff_lon_min)
    if dropoff_lon_max:
        filters.append(Trip.dropoff_longitude <= dropoff_lon_max)
    if store_and_fwd_flag:
        filters.append(Trip.store_and_fwd_flag == store_and_fwd_flag)

    # Apply filters
    for filter_condition in filters:
        count_query = count_query.where(filter_condition)
        data_query = data_query.where(filter_condition)

    # Get total count
    total_count = session.exec(count_query).one()

    # Apply sorting
    from sqlalchemy import asc as sa_asc
    from sqlalchemy import desc as sa_desc

    sort_fields = {
        SortField.pickup_datetime: Trip.pickup_datetime,
        SortField.dropoff_datetime: Trip.dropoff_datetime,
        SortField.trip_duration: Trip.trip_duration,
        SortField.passenger_count: Trip.passenger_count,
    }
    sort_column = sort_fields.get(sort_by, Trip.pickup_datetime)
    order_func = sa_desc if sort_order == SortOrder.desc else sa_asc
    data_query = data_query.order_by(order_func(col(sort_column)))

    # Apply pagination
    data_query = data_query.offset(skip).limit(limit)

    # Execute query
    trips = session.exec(data_query).all()

    # Calculate pagination metadata
    current_page = (skip // limit) + 1
    total_pages = (total_count + limit - 1) // limit  # Ceiling division
    has_next = skip + limit < total_count
    has_prev = skip > 0

    return TripsResponse(
        message="Fetched trips successfully",
        success=True,
        data=list(trips),
        pagination=PaginationMeta(
            total=total_count,
            page=current_page,
            page_size=limit,
            total_pages=total_pages,
            has_next=has_next,
            has_prev=has_prev,
        ),
    )


# endregion


# region "/trips/{trip_id}"
class TripByIdResponse(BaseResponse):
    data: Trip


@app.get("/api/trips/{trip_id}")
async def get_trip_by_id(
    trip_id: str,
    session: Session = Depends(get_session),
) -> TripByIdResponse:
    """Get a specific trip by ID."""
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")
    return TripByIdResponse(
        data=trip, message="Trip fetched successfully", success=True
    )


# endregion


# region "/api/analytics/stats"
class TripStatsResponse(BaseResponse):
    data: TripStats


@app.get("/api/analytics/stats")
async def get_statistics(
    pickup_start: Optional[datetime] = Query(None),
    pickup_end: Optional[datetime] = Query(None),
    session: Session = Depends(get_session),
) -> TripStatsResponse:
    """
    Get overall statistics for trips.

    Provides:
    - Total trips count
    - Average, median, min, max duration
    - Average passengers per trip
    - Total passengers transported

    Optimized with database-level aggregations.
    """
    # Build base query with filters
    query = select(
        func.count(col(Trip.id)).label("total_trips"),
        func.sum(col(Trip.trip_duration)).label("total_duration"),
        func.sum(col(Trip.passenger_count)).label("total_passengers"),
    )

    if pickup_start:
        query = query.where(Trip.pickup_datetime >= pickup_start)
    if pickup_end:
        query = query.where(Trip.pickup_datetime <= pickup_end)

    result = session.exec(query).first()

    if not result or result.total_trips == 0:
        raise HTTPException(status_code=404, detail="No trips found matching criteria")

    return TripStatsResponse(
        data=TripStats(
            total_trips=result.total_trips,
            total_duration=float(result.total_duration),
            total_passengers=result.total_passengers,
        ),
        message="Statistics fetched successfully",
        success=True,
    )


# endregion


# region "/api/analytics/time-series"
class timeRange(Enum):
    last_7_days = "7d"
    last_30_days = "30d"
    last_3_months = "3m"
    all_time = "all"


class TimeSeriesResponse(BaseResponse):
    data: list[TimeSeriesPoint]


@app.get("/api/analytics/time-series")
async def get_time_series(
    time_range: Optional[str] = Query(
        None,
        description="Time range: '7d' (last 7 days), '30d' (last 30 days), '3m' (last 3 months), 'all' (all time)",
    ),
    interval: str = Query(
        "day",
        description="Aggregation interval: 'hour' or 'day'. Default: 'day' for better visualization",
    ),
    session: Session = Depends(get_session),
) -> TimeSeriesResponse:
    """
    Time series data for trend analysis and visualization (like the graph shown).

    Perfect for plotting:
    - Trip volume over time
    - Demand patterns
    - Trend comparison across periods

    Returns data points that can be plotted as a line/area chart.
    Optimized with database-level aggregation using date_trunc.
    """
    from datetime import timedelta

    from sqlalchemy import text

    # Calculate date filter based on time_range
    # Get the latest date from the database first
    pickup_start = None
    if time_range in ["7d", "30d", "3m"]:
        max_date_sql = text("SELECT MAX(pickup_datetime) as max_date FROM trips")
        max_date_result = session.execute(max_date_sql).first()

        if max_date_result and max_date_result.max_date:  # type: ignore
            max_date = max_date_result.max_date  # type: ignore

            if time_range == "7d":
                # Last 7 days from latest date in database
                pickup_start = max_date - timedelta(days=7)
                interval = "hour"  # Use hourly for 7 days for more granularity
            elif time_range == "30d":
                # Last 30 days from latest date in database
                pickup_start = max_date - timedelta(days=30)
                interval = "day"  # Use daily for 30 days
            elif time_range == "3m":
                # Last 3 months (90 days) from latest date in database
                pickup_start = max_date - timedelta(days=90)
                interval = "day"  # Use daily for 3 months
    # 'all' or None means no date filter, use daily by default

    # Use PostgreSQL's date_trunc for efficient time bucketing
    sql = text(
        """
        SELECT 
            date_trunc(:interval, pickup_datetime) as time_bucket,
            COUNT(*) as trip_count,
            AVG(trip_duration) as avg_duration
        FROM trips
        WHERE (:pickup_start IS NULL OR pickup_datetime >= :pickup_start)
        GROUP BY date_trunc(:interval, pickup_datetime)
        ORDER BY time_bucket
    """
    )

    results = session.execute(
        sql, {"interval": interval, "pickup_start": pickup_start}
    ).all()

    if not results:
        raise HTTPException(status_code=404, detail="No trips found")

    return TimeSeriesResponse(
        data=[
            TimeSeriesPoint(
                timestamp=row.time_bucket,  # type: ignore
                trip_count=row.trip_count,  # type: ignore
                avg_duration=float(row.avg_duration),  # type: ignore
            )
            for row in results
        ],
        message="Time series data fetched successfully",
        success=True,
    )


# endregion
