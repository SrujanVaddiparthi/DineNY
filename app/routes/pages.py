"""

"""

from fastapi import APIRouter, Request, Query, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.search_service import search_restaurants
from app.services.restaurant_service import (
    get_restaurant_by_id,
    add_comment_to_restaurant,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/search", response_class=HTMLResponse)
def search_page(
    request: Request,
    q: str = Query(default=""),
):
    results = search_restaurants(q) if q.strip() else []

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "query": q,
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