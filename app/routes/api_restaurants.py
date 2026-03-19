from fastapi import APIRouter, HTTPException

from app.services.restaurant_service import get_restaurant_by_id

router = APIRouter(prefix="/api", tags=["api-restaurants"])


@router.get("/restaurants/{restaurant_id}")
def api_restaurant_detail(restaurant_id: str):
    restaurant = get_restaurant_by_id(restaurant_id)

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return restaurant