# DineNY

DineNY is a MongoDB-based restaurant search application focused on restaurants in the NYC / nearby metro area.  
The project supports text search, restaurant detail viewing, comments, geospatial querying, and later GridFS-backed image handling.

---

## Current Backend Progress

The following backend pieces are currently implemented:

- cleaned MongoDB collection: `restaurants_clean`
- normalized searchable field: `search_blob`
- GeoJSON `location` field
- 2dsphere index on `location`
- FastAPI backend
- search page
- search results page
- restaurant detail page
- comment submission and retrieval
- JSON API routes:
  - `GET /api/search?q=<term>`
  - `GET /api/restaurants/{id}`

---

## Project Structure

```text
DineNY/
├── app/
│   ├── main.py
│   ├── db.py
│   ├── routes/
│   ├── services/
│   ├── templates/
│   └── static/
├── scripts/
├── docs/
├── data/
└── notebooks/
```

---

## Local Setup

```bash
git clone <repo>
cd DineNY

python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Running the App

```bash
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000  
- http://127.0.0.1:8000/health  

---

## MongoDB Requirements

- URI: `mongodb://localhost:27017`
- Database: `dineny`

Collections:
- `restaurants`
- `restaurants_clean`

---

## Data Setup Workflow

### 1. Import CSV

```bash
mongoimport \
  --db dineny \
  --collection restaurants \
  --type csv \
  --headerline \
  --file data/scaled/nyc_restaurants_no_mcD.csv
```

### 2. Build cleaned collection

```bash
python scripts/build_clean_collection.py
```

### 3. Create geo index

```bash
python scripts/create_indexes.py
```

---

## Routes Overview

### HTML Routes

- `/`
- `/search?q=`
- `/restaurants/{id}`
- `POST /restaurants/{id}/comments`

### API Routes

- `/api/search?q=`
- `/api/restaurants/{id}`

---

## Example API Usage

**Search**
```
http://127.0.0.1:8000/api/search?q=thai
```

**Restaurant**
```
http://127.0.0.1:8000/api/restaurants/<id>
```

---

## Documentation

- `docs/backend_progress_notes.md`
- `docs/frontend_api_contract.md`
- `docs/frontend_flow_notes.md`

---

## Notes

- Jinja templates are for demo/testing only  
- Frontend should use API routes  