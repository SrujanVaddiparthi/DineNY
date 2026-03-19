"""

"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import pages, api_search, api_restaurants

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages.router)
app.include_router(api_search.router)
app.include_router(api_restaurants.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}