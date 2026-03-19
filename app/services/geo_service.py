from app.db import db


def get_nearby_restaurants(lat: float, lon: float, radius_meters: int = 2000):
    collection = db["restaurants_clean"]

    results = collection.aggregate([
        {
            "$geoNear": {
                "near": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "distanceField": "distance",
                "maxDistance": radius_meters,
                "spherical": True
            }
        },
        {
            "$project": {
                "_id": 1,
                "title": 1,
                "category": 1,
                "rating": 1,
                "address": 1,
                "latitude": 1,
                "longitude": 1,
                "distance": 1
            }
        },
        {
            "$limit": 25
        }
    ])

    restaurants = []
    for r in results:
        restaurants.append({
            "id": str(r["_id"]),
            "title": r.get("title"),
            "category": r.get("category"),
            "rating": r.get("rating"),
            "address": r.get("address"),
            "latitude": r.get("latitude"),
            "longitude": r.get("longitude"),
            "distance_meters": round(r.get("distance", 0), 2)
        })

    return restaurants