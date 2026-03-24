"""

"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://mongoapp:huMONGOu5@localhost:27017/dineny?authSource=dineny",
)
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "dineny")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]


def get_collection(name: str):
    return db[name]