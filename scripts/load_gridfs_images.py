# needed to store images in mongodb itself using gridfs
import os
import mimetypes
import requests
import gridfs

from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "dineny"
COLLECTION_NAME = "restaurants_clean"

MAX_RESTAURANTS = 1000
REQUEST_TIMEOUT = 15


def main():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    fs = gridfs.GridFS(db)

    query = {
        "primary_image_gridfs_id": None,
        "image_urls.0.thumbnail": {"$exists": True}
    }

    cursor = collection.find(query).limit(MAX_RESTAURANTS)

    success_count = 0
    fail_count = 0
    skipped_count = 0

    for doc in cursor:
        restaurant_id = doc["_id"]
        title = doc.get("title", "restaurant")
        image_urls = doc.get("image_urls", [])

        if not image_urls:
            skipped_count += 1
            continue

        thumbnail_url = None
        for image in image_urls:
            if image.get("thumbnail"):
                thumbnail_url = image["thumbnail"]
                break

        if not thumbnail_url:
            skipped_count += 1
            continue

        try:
            response = requests.get(thumbnail_url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "image/jpeg")
            extension = mimetypes.guess_extension(content_type.split(";")[0]) or ".jpg"
            filename = f"{title.replace('/', '_')}{extension}"

            file_id = fs.put(
                response.content,
                filename=filename,
                content_type=content_type,
                restaurant_id=str(restaurant_id),
                source_url=thumbnail_url,
            )

            collection.update_one(
                {"_id": restaurant_id},
                {"$set": {"primary_image_gridfs_id": file_id}}
            )

            success_count += 1
            print(f"[OK] Stored GridFS image for {title}")

        except Exception as e:
            fail_count += 1
            print(f"[FAIL] {title}: {e}")

    print("\nDone.")
    print(f"Success: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"Skipped: {skipped_count}")


if __name__ == "__main__":
    main()