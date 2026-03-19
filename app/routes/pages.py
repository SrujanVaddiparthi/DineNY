from fastapi import APIRouter, Request, Query, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.search_service import search_restaurants_with_geo
from app.services.restaurant_service import (
    get_restaurant_by_id,
    add_comment_to_restaurant,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


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


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/search", response_class=HTMLResponse)
def search_page(
    request: Request,
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

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "query": q,
            "lat": parsed_lat,
            "lon": parsed_lon,
            "radius": parsed_radius,
            "min_rating": parsed_min_rating,
            "max_rating": parsed_max_rating,
            "results": results,
        },
    )


@router.get("/restaurants/{restaurant_id}", response_class=HTMLResponse)
def restaurant_detail(request: Request, restaurant_id: str):
    restaurant = get_restaurant_by_id(restaurant_id)

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return templates.TemplateResponse(
        "details.html",
        {
            "request": request,
            "restaurant": restaurant,
        },
    )


@router.post("/restaurants/{restaurant_id}/comments")
def add_comment(
    restaurant_id: str,
    author: str = Form(default="Anonymous"),
    text: str = Form(...),
):
    success = add_comment_to_restaurant(restaurant_id, author, text)

    if not success:
        raise HTTPException(status_code=400, detail="Failed to add comment")

    return RedirectResponse(
        url=f"/restaurants/{restaurant_id}",
        status_code=303,
    )