from __future__ import annotations

from typing import Any, Optional
from datetime import datetime, timezone

from bson import ObjectId
from app.db import get_collection


def build_primary_image_src(doc: dict[str, Any]) -> str | None:
    primary_image_gridfs_id = doc.get("primary_image_gridfs_id")
    if primary_image_gridfs_id:
        return f"/api/images/{primary_image_gridfs_id}"

    image_urls = doc.get("image_urls", [])
    if image_urls and image_urls[0].get("thumbnail"):
        return image_urls[0]["thumbnail"]

    return None


def get_restaurant_by_id(restaurant_id: str) -> Optional[dict[str, Any]]:
    col = get_collection("restaurants_clean")

    doc = col.find_one({"_id": ObjectId(restaurant_id)})
    if not doc:
        return None

    restaurant = {
        "id": str(doc["_id"]),
        "title": doc.get("title"),
        "category": doc.get("category"),
        "rating": doc.get("rating"),
        "website": doc.get("website"),
        "phone": doc.get("phone"),
        "address": doc.get("address"),
        "categories": doc.get("categories", []),
        "image_urls": doc.get("image_urls", []),
        "primary_image_gridfs_id": str(doc["primary_image_gridfs_id"]) if doc.get("primary_image_gridfs_id") else None,
        "primary_image_src": build_primary_image_src(doc),
        "latitude": doc.get("latitude"),
        "longitude": doc.get("longitude"),
        "location": doc.get("location"),
        "comments": doc.get("comments", []),
    }

    return restaurant


def add_comment_to_restaurant(
    restaurant_id: str,
    author: str,
    text: str,
) -> bool:
    col = get_collection("restaurants_clean")

    author = author.strip() if author else "Anonymous"
    text = text.strip()

    if not text:
        return False

    comment = {
        "author": author or "Anonymous",
        "text": text,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    result = col.update_one(
        {"_id": ObjectId(restaurant_id)},
        {"$push": {"comments": comment}},
    )

    return result.modified_count == 1