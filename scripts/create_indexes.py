"""
without this index mongo cannot run $near or $geoWithin
the geo search will fail
hence must do this to unlock:
- restaurants near lat/lon
- radius queries
- map-based filtering
"""

import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "dineny"
COLLECTION = "restaurants_clean"

def main():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    col = db[COLLECTION]

    print("Creating 2dsphere index on location...")

    col.create_index([("location", "2dsphere")])

    print("Index created successfully!")

if __name__ == "__main__":
    main()