import gridfs
from bson import ObjectId

from app.db import db


def get_gridfs_file(file_id: str):
    fs = gridfs.GridFS(db)
    return fs.get(ObjectId(file_id))