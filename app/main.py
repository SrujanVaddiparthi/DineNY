from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import api_search, api_restaurants, api_geo, api_images

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_search.router)
app.include_router(api_restaurants.router)
app.include_router(api_geo.router)
app.include_router(api_images.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}