"""

"""

from fastapi import APIRouter, Query

from app.services.search_service import search_restaurants

router = APIRouter(prefix="/api", tags=["api-search"])


@router.get("/search")
def api_search(q: str = Query(default="")):
    if not q.strip():
        return []

    return search_restaurants(q)