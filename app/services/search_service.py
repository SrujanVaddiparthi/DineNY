from __future__ import annotations

from typing import Any

from app.db import get_collection


def search_restaurants(query: str, limit: int = 100) -> list[dict[str, Any]]:
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


def search_restaurants_with_geo(
    query: str = "",
    lat: float | None = None,
    lon: float | None = None,
    radius: int = 2000,
    min_rating: float | None = None,
    max_rating: float | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    col = get_collection("restaurants_clean")

    pipeline = []

    rating_filter: dict[str, Any] = {}
    if min_rating is not None:
        rating_filter["$gte"] = min_rating
    if max_rating is not None:
        rating_filter["$lte"] = max_rating

    if lat is not None and lon is not None:
        geo_query: dict[str, Any] = {}

        if rating_filter:
            geo_query["rating"] = rating_filter

        if query.strip():
            geo_query["search_blob"] = {
                "$regex": query.strip(),
                "$options": "i",
            }

        geo_stage = {
            "$geoNear": {
                "near": {
                    "type": "Point",
                    "coordinates": [lon, lat],
                },
                "distanceField": "distance",
                "maxDistance": radius,
                "spherical": True,
            }
        }

        if geo_query:
            geo_stage["$geoNear"]["query"] = geo_query

        pipeline.append(geo_stage)

    elif query.strip() or rating_filter:
        match_stage: dict[str, Any] = {}

        if query.strip():
            match_stage["search_blob"] = {
                "$regex": query.strip(),
                "$options": "i",
            }

        if rating_filter:
            match_stage["rating"] = rating_filter

        pipeline.append({"$match": match_stage})

    else:
        return []

    pipeline.extend(
        [
            {"$sort": {"rating": -1}},
            {"$limit": limit},
            {
                "$project": {
                    "_id": 1,
                    "title": 1,
                    "category": 1,
                    "rating": 1,
                    "address": 1,
                    "latitude": 1,
                    "longitude": 1,
                    "image_urls": 1,
                    "primary_image_gridfs_id": 1,
                    "distance": 1,
                }
            },
        ]
    )

    cursor = col.aggregate(pipeline)

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
                "distance_meters": round(doc.get("distance", 0), 2)
                if doc.get("distance") is not None else None,
            }
        )

    return results