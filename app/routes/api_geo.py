from fastapi import APIRouter, Query
from app.services.geo_service import get_nearby_restaurants

router = APIRouter(prefix="/api", tags=["api-geo"])


@router.get("/nearby")
def nearby_restaurants(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    radius: int = Query(2000, description="Search radius in meters"),
):
    results = get_nearby_restaurants(lat, lon, radius)
    return {"results": results}