# DineNY

DineNY is a MongoDB + FastAPI + React/Vite application for restaurant search in New York State. It supports text and geo search, rating filters, sorting, map visualization, detail pages, image serving from GridFS, and user comments.

---

## Live Site
- App: https://dineny.webdev.gccis.rit.edu/
- API base (via Nginx): https://dineny.webdev.gccis.rit.edu/api

---

## Assignment Readme Requirements

1) **Technology Stack (and why)**  
- **Backend:** FastAPI + Uvicorn (fast API development, easy JSON endpoints), PyMongo (direct MongoDB integration), MongoDB with 2dsphere indexing (native geospatial search) and GridFS (image storage).  
- **Frontend:** React + Vite (fast development/build workflow), Leaflet / react-leaflet (interactive maps), Axios (API requests).  
- **Infrastructure / Deployment:** Python 3.10+, Node.js 22+, MongoDB, and VM deployment on RLES. Reverse proxy / service setup used for running the application on the VM.

2) **Process (loading + cleansing)**  
- Started with a large [raw CSV dataset](https://www.kaggle.com/datasets/kwxdata/380k-restaurants-mostly-usa-based) of restaurant records and filtered it down to New York State / nearby metro area restaurants using an ETL notebook.  
- Removed irrelevant records and handled noisy data, including inconsistent casing, extra whitespace, missing values, and invalid fields.  
- Imported the filtered CSV into MongoDB as the raw `restaurants` collection using `mongoimport`.  
- Built a cleaned backend-ready collection called `restaurants_clean` using a Python transformation script.  
- Standardized fields such as title, category, address, and rating, and created a combined `search_blob` field to support partial text search across restaurant name, cuisine, and address.  
- Converted latitude and longitude into GeoJSON `location` objects for geospatial querying, and created a `2dsphere` index to support radius-based search.  
- Stored a subset of restaurant images in MongoDB GridFS and linked them back to restaurant documents through `primary_image_gridfs_id`.  
- Enabled MongoDB authentication by creating a scoped application user and updating the backend to connect using credentials.

**Problems encountered and fixes**
- The raw dataset contained inconsistent address formats, duplicate restaurant records, missing ratings, and invalid or swapped coordinates.  
- Some image URLs were broken or unavailable, so image ingestion into GridFS had partial failures; we handled this by storing a valid subset and falling back gracefully when needed.  
- We also ran into authentication-related issues after enabling MongoDB authorization; these were resolved by updating the backend connection string and using a dedicated MongoDB user with the required permissions.

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
- Combined **text search and geospatial search** using MongoDB’s 2dsphere indexing and flexible query design.  
- Integrated **interactive map visualization** with live backend-driven results.  
- Implemented **GridFS-based image storage** with graceful fallback to external image URLs when needed.  
- Designed a flexible backend supporting **optional filters** such as min/max rating for extensibility.  
- Built a clean **API-first architecture**, allowing a React frontend to fully consume backend services.  
- Transitioned from a temporary server-rendered UI to a **modern React-based frontend**, improving scalability and separation of concerns.  
- Deployed the application on a VM with working backend–frontend integration.
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

7) **Remote access & SSH tunneling**
```bash
# Shell into server (custom port)
ssh student@dineny.webdev.gccis.rit.edu -p 22070

# Forward local port 27017 to remote Mongo
ssh -L 27017:localhost:27017 -p 22070 student@dineny.webdev.gccis.rit.edu

# Forward local 8000 to hit FastAPI directly (bypass Nginx) if debugging
ssh -L 8000:localhost:8000 -p 22070 student@dineny.webdev.gccis.rit.edu
```
Nginx already exposes `/api` and the frontend on 80/443, so tunnels are only needed for direct backend/Mongo access.

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