# DineNY

DineNY is a MongoDB + FastAPI + React/Vite application for restaurant search in New York State. It supports text and geo search, rating filters, sorting, map visualization, detail pages, image serving from GridFS, and user comments.

---

## Assignment Readme Requirements

1) **Technology Stack (and why)**  
- Backend: FastAPI + Uvicorn (fast, async, easy JSON APIs), MongoDB with 2dsphere (native geo search) + GridFS (image storage).  
- Frontend: React + Vite (fast dev/build), react-leaflet/Leaflet (battle-tested mapping), Axios (HTTP).  
- Infra: Node 22+ / Python 3.10+, Nginx (reverse proxy), systemd (service management).

2) **Process (loading + cleansing)**  
- Imported raw CSV of NY restaurants into MongoDB (`restaurants`).  
- Cleaned into `restaurants_clean`: standardized casing, trimmed whitespace, normalized ratings, built `search_blob` for text search.  
- Converted lat/lon into GeoJSON `location`, fixed swapped/invalid coords, dropped rows without usable coordinates.  
- Created 2dsphere index on `location` to enable geo queries.  
- Handled missing images by allowing empty `primary_image_src`; GridFS used for stored images.  
- Common issues: inconsistent address formats, missing/zero coordinates, duplicate records—mitigated via basic de-dupe and null/zero guards.

3) **Volume (collection sizes)**  

```bash
db.restaurants_clean.countDocuments();
7294
```

4) **Variety (interesting searches)**  
Sample queries that surface diverse results:  
- "halal" (Queens / Brooklyn clusters)  
- "ramen" (Manhattan/Jersey City mix)  
- "gluten free" (Brooklyn/Manhattan)  
- "colombian" (Jackson Heights area)  
- "bagel" (city-wide)  
- Geo + cuisine: search "tacos" then drag/zoom map near Sunset Park or Jackson Heights.  
- Rating filters: min 4.0 + cuisine (e.g., "sushi") to see high-rated spots.

5) **Bells and Whistles (what we’re proud of)**  
- Integrated map view with clustered markers via Leaflet.  
- Geo + text search with rating filters and sorting.  
- Detail view with images (GridFS-backed) and live comments.  
- Clean UI (React/Vite), responsive layout, quick search bar + inline filters.  
- API-first design: consistent JSON routes for frontend/other clients.

---

## Project Structure (high level)
```text
DineNY/
├── app/               # FastAPI app, routes, services
├── frontend/          # React/Vite frontend (src, public)
├── notebooks/         # Data prep/ETL notebooks
├── requirements.txt   # Python deps
├── package.json       # Frontend scripts
└── README.md
```

---

## Core Features
- Text search by name/cuisine/address
- Geo search by lat/lon + radius
- Rating filters (min/max), sorting
- Results list + map with markers
- Detail view with images (GridFS) and comments
- Image endpoint: `/api/images/{file_id}`
- Commenting: `POST /api/restaurants/{id}/comments`

---

## API Routes (JSON)
- `GET /api/search?q=<term>&lat=<lat>&lon=<lon>&radius=<meters>&min_rating=&max_rating=`
- `GET /api/restaurants/{id}`
- `POST /api/restaurants/{id}/comments` (JSON body: `{ author, text }`)
- `GET /api/images/{file_id}`

---

## Prerequisites
- Python 3.10+
- Node.js 22.x (or 20.19+), npm
- MongoDB 6+

---

## Local Setup (dev)
```bash
git clone <repo>
cd DineNY

python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cd frontend
npm install
npm run dev                 # frontend at http://localhost:5173
# in another shell (back at repo root with venv):
uvicorn app.main:app --reload --port 8000  # API at http://localhost:8000
```

Set `VITE_API_BASE` in a `.env` (frontend) if your API is not on http://localhost:8000.

---

## Production Build & Deploy (summary)
1) **Backend service (systemd)**
```bash
python3 -m venv /opt/DineNY/.venv
source /opt/DineNY/.venv/bin/activate
pip install -r requirements.txt

# /etc/systemd/system/dineny-backend.service
[Unit]
Description=DineNY FastAPI
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/DineNY
Environment="PATH=/opt/DineNY/.venv/bin"
ExecStart=/opt/DineNY/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now dineny-backend
```

2) **Frontend build**
```bash
cd frontend
npm install
npm run build   # outputs dist/
```

3) **Nginx reverse proxy**
```nginx
server {
    listen 80;
    server_name your-domain-or-ip;

    root /opt/DineNY/frontend/dist;
    index index.html;

    location / {
        try_files $uri /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
```bash
sudo ln -s /etc/nginx/sites-available/dineny /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx
```

4) **MongoDB**
- Connection string: `MONGO_URI` (e.g., `mongodb://localhost:27017` or Atlas URI)
- Database: `dineny`
- Collections: `restaurants`, `restaurants_clean`
- Ensure 2dsphere index on `location`

5) **Environment**
- Backend `.env` (if used):
  - `MONGO_URI=`
  - `MONGO_DB=dineny`
- Frontend `.env` (optional):
  - `VITE_API_BASE=https://your-domain-or-ip`

6) **Updating**
```bash
cd /opt/DineNY
git pull
cd frontend && npm run build && cd ..
sudo systemctl restart dineny-backend
sudo systemctl reload nginx
```

---

## Data Prep (optional)
- `mongoimport` raw CSV to `restaurants`
- `scripts/build_clean_collection.py` to generate `restaurants_clean`
- `scripts/create_indexes.py` to set 2dsphere index

---

## Frontend Notes
- Map uses react-leaflet; ensure Leaflet CSS is imported (already in `src/main.jsx`).
- API client lives in `frontend/src/api/api.js` and expects `/api` proxied to FastAPI.

---

## Useful Commands
- Dev API: `uvicorn app.main:app --reload --port 8000`
- Dev frontend: `npm run dev -- --host`
- Build frontend: `npm run build`
- Prod API (behind Nginx): systemd service `dineny-backend`

---

## License
MIT