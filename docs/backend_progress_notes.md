# Backend Progress Notes

## Current Backend Status

The backend currently supports:

- MongoDB connection
- Search using `search_blob`
- Results page
- Restaurant detail page
- Comment submission and retrieval
- JSON API routes

---

## Important Collections

### restaurants
Raw imported dataset.

### restaurants_clean
Processed dataset used by backend.

Includes:
- cleaned categories
- image metadata
- GeoJSON `location`
- `search_blob`
- `comments`

---

## Key Files

### Core
- app/main.py
- app/db.py

### Routes
- app/routes/pages.py
- app/routes/api_search.py
- app/routes/api_restaurants.py

### Services
- app/services/search_service.py
- app/services/restaurant_service.py

### Scripts
- scripts/build_clean_collection.py
- scripts/create_indexes.py

---

## How to Run

```bash
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## What to Test

### Pages
- `/`
- search (thai, halal, indian)
- open any restaurant

### APIs
- `/api/search?q=thai`
- `/api/restaurants/<id>`

### Comments
- open restaurant page
- add comment
- confirm it appears

---

## Do NOT Modify

- collection schema (`restaurants_clean`)
- route paths
- JSON response structure
- scripts in `/scripts`

---

## Tasks for Backend Teammate

- Clean route files
- Ensure consistent JSON responses
- Test all endpoints
- Add validation (empty input, invalid IDs)
- Document API responses

---

## Next Features

- geospatial search
- map integration
- GridFS images