from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import pages, api_search, api_restaurants, api_geo, api_images

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages.router)
app.include_router(api_search.router)
app.include_router(api_restaurants.router)
app.include_router(api_geo.router)
app.include_router(api_images.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}