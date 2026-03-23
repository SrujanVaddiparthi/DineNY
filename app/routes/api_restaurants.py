from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.restaurant_service import (
    get_restaurant_by_id,
    add_comment_to_restaurant,
)

router = APIRouter(prefix="/api", tags=["api-restaurants"])


@router.get("/restaurants/{restaurant_id}")
def api_restaurant_detail(restaurant_id: str):
    restaurant = get_restaurant_by_id(restaurant_id)

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return restaurant


class CommentPayload(BaseModel):
    author: str | None = None
    text: str


@router.post("/restaurants/{restaurant_id}/comments")
def api_add_comment(restaurant_id: str, payload: CommentPayload):
    success = add_comment_to_restaurant(
        restaurant_id=restaurant_id,
        author=(payload.author or "Anonymous"),
        text=payload.text,
    )

    if not success:
        raise HTTPException(status_code=400, detail="Failed to add comment")

    restaurant = get_restaurant_by_id(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return {"comments": restaurant.get("comments", [])}