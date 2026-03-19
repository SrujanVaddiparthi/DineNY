from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.services.image_service import get_gridfs_file

router = APIRouter(prefix="/api", tags=["api-images"])


@router.get("/images/{file_id}")
def serve_image(file_id: str):
    try:
        grid_out = get_gridfs_file(file_id)
        return Response(
            content=grid_out.read(),
            media_type=getattr(grid_out, "content_type", "image/jpeg")
        )
    except Exception:
        raise HTTPException(status_code=404, detail="Image not found")