from fastapi import APIRouter, Query

from app.services.search_service import search_restaurants_with_geo

router = APIRouter(prefix="/api", tags=["api-search"])


def parse_optional_float(value: str | None):
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    return float(value)


def parse_optional_int(value: str | None, default: int = 2000):
    if value is None:
        return default
    value = value.strip()
    if value == "":
        return default
    return int(value)


@router.get("/search")
def api_search(
    q: str = Query(default=""),
    lat: str | None = Query(default=None),
    lon: str | None = Query(default=None),
    radius: str | None = Query(default="2000"),
    min_rating: str | None = Query(default=None),
    max_rating: str | None = Query(default=None),
):
    parsed_lat = parse_optional_float(lat)
    parsed_lon = parse_optional_float(lon)
    parsed_radius = parse_optional_int(radius, default=2000)
    parsed_min_rating = parse_optional_float(min_rating)
    parsed_max_rating = parse_optional_float(max_rating)

    results = search_restaurants_with_geo(
        query=q,
        lat=parsed_lat,
        lon=parsed_lon,
        radius=parsed_radius,
        min_rating=parsed_min_rating,
        max_rating=parsed_max_rating,
    )

    return {"results": results}