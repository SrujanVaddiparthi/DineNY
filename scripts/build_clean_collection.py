# This script will:
# connect to MongoDB
# read from raw restaurants
# parse string fields like Images, Categories, Geo_Coordinates
# create location
# create search_blob
# initialize comments
# write into restaurants_clean
from __future__ import annotations

import ast
import os
import re
from typing import Any, Optional

from pymongo import MongoClient
from bson import ObjectId


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "dineny"
SOURCE_COLLECTION = "restaurants"
TARGET_COLLECTION = "restaurants_clean"


def safe_literal_eval(value: Any) -> Any:
    """Safely parse stringified Python literals like lists/dicts."""
    if value is None:
        return None
    if not isinstance(value, str):
        return value

    value = value.strip()
    if not value:
        return None

    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value


def normalize_text(value: Any) -> str:
    """Lowercase and remove extra punctuation/whitespace for search."""
    if value is None:
        return ""

    text = str(value).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_search_blob(
    title: str,
    category: str,
    categories: list[str],
    address: str,
) -> str:
    parts = [
        normalize_text(title),
        normalize_text(category),
        normalize_text(" ".join(categories)),
        normalize_text(address),
    ]
    return " ".join(part for part in parts if part).strip()


def parse_categories(raw_categories: Any) -> list[str]:
    parsed = safe_literal_eval(raw_categories)

    if parsed is None:
        return []

    if isinstance(parsed, list):
        return [str(x).strip() for x in parsed if str(x).strip()]

    if isinstance(parsed, str):
        cleaned = parsed.strip()
        return [cleaned] if cleaned else []

    return []


def parse_images(raw_images: Any) -> list[dict[str, Any]]:
    parsed = safe_literal_eval(raw_images)

    if parsed is None:
        return []

    if isinstance(parsed, list):
        cleaned_images: list[dict[str, Any]] = []
        for item in parsed:
            if isinstance(item, dict):
                cleaned_images.append(
                    {
                        "thumbnail": item.get("thumbnail"),
                        "title": item.get("title"),
                    }
                )
        return cleaned_images

    return []


def parse_float(value: Any) -> Optional[float]:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (ValueError, TypeError):
        return None


def build_location(longitude: Optional[float], latitude: Optional[float]) -> Optional[dict[str, Any]]:
    if longitude is None or latitude is None:
        return None

    return {
        "type": "Point",
        "coordinates": [longitude, latitude],
    }


def transform_document(doc: dict[str, Any]) -> dict[str, Any]:
    title = doc.get("Title", "")
    category = doc.get("Category", "")
    rating = parse_float(doc.get("Rating"))
    website = doc.get("Website")
    phone = doc.get("Phone")
    address = doc.get("Address", "")

    categories = parse_categories(doc.get("Categories"))
    image_urls = parse_images(doc.get("Images"))

    latitude = parse_float(doc.get("Latitude"))
    longitude = parse_float(doc.get("Longitude"))

    clean_doc = {
        "source_restaurant_id": doc.get("_id"),
        "title": title,
        "category": category,
        "rating": rating,
        "website": website,
        "phone": phone,
        "address": address,
        "categories": categories,
        "image_urls": image_urls,
        "primary_image_gridfs_id": None,
        "latitude": latitude,
        "longitude": longitude,
        "location": build_location(longitude, latitude),
        "search_blob": build_search_blob(title, category, categories, address),
        "comments": [],
    }

    return clean_doc


def main() -> None:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    source = db[SOURCE_COLLECTION]
    target = db[TARGET_COLLECTION]

    print(f"Connected to MongoDB: {MONGO_URI}")
    print(f"Reading from: {DB_NAME}.{SOURCE_COLLECTION}")
    print(f"Writing to:   {DB_NAME}.{TARGET_COLLECTION}")

    target.drop()
    print("Dropped existing target collection (if any).")

    batch: list[dict[str, Any]] = []
    count = 0
    batch_size = 500

    for doc in source.find({}):
        clean_doc = transform_document(doc)
        batch.append(clean_doc)

        if len(batch) >= batch_size:
            target.insert_many(batch)
            count += len(batch)
            print(f"Inserted {count} cleaned documents...")
            batch = []

    if batch:
        target.insert_many(batch)
        count += len(batch)

    print(f"Finished. Total cleaned documents inserted: {count}")


if __name__ == "__main__":
    main()