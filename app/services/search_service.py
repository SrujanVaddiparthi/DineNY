"""

"""

from __future__ import annotations

from typing import Any

from app.db import get_collection


def search_restaurants(query: str, limit: int = 50) -> list[dict[str, Any]]:
    col = get_collection("restaurants_clean")

    cleaned_query = query.strip()
    if not cleaned_query:
        return []

    cursor = (
        col.find(
            {
                "search_blob": {
                    "$regex": cleaned_query,
                    "$options": "i",
                }
            }
        )
        .sort("rating", -1)
        .limit(limit)
    )

    results = []
    for doc in cursor:
        results.append(
            {
                "id": str(doc["_id"]),
                "title": doc.get("title"),
                "category": doc.get("category"),
                "rating": doc.get("rating"),
                "address": doc.get("address"),
                "has_image": bool(doc.get("primary_image_gridfs_id") or doc.get("image_urls")),
                "latitude": doc.get("latitude"),
                "longitude": doc.get("longitude"),
            }
        )

    return results