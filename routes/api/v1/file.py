from fastapi import APIRouter, HTTPException, status
from fastapi import File, UploadFile
from services import gemini
from utils.file import save_file, delete_file
from models.responses import BaseResponse
import os
from helpers import chat
from logging import getLogger
from middleware import validate_user

logger = getLogger(__name__)

ALLOWED_MIME_TYPES = [
    "image/jpeg",
    "image/png",
    "image/jpg",
    "image/webp",
]


FILE_ANALYZE_PROMPT = os.getenv("FILE_ANALYZE_PROMPT")

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


file_router = APIRouter()


@file_router.post("/analyze/{user_id}", response_model=BaseResponse)
@validate_user.validate
async def upload_file(file: UploadFile = File(...), user_id: str = None):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not allowed",
        )
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size too large",
        )
    path = save_file(file)
    try:
        res = gemini.analyze_image(path, FILE_ANALYZE_PROMPT)
        delete_file(path)
        exits_user_data = chat.exits_user_data(user_id)
        if exits_user_data:
            chat.reset_user_data(user_id)
        chat.add_data_to_cache(user_id, {"role": "model", "parts": res})
        return {"data": res}
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
