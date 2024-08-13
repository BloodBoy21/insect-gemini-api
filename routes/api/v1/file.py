from fastapi import APIRouter, HTTPException, status
from fastapi import File, UploadFile
from services import gemini
from utils.file import save_file, delete_file
from models.responses import BaseResponse, ErrorResponse
import os

ALLOWED_MIME_TYPES = [
    "image/jpeg",
    "image/png",
    "image/jpg",
    "image/webp",
]

DEFAULT_PROMPT = """
Analyze the image and check if this is an insect or not.

If it is an insect, return the following schema:

{
    "isInsect": Boolean,
    "name": "name of the insect",
    "description": "description of the insect",
    "scientificName": "scientific name of the insect",
    "family": "family of the insect",
    "isDangerous": Boolean,
    "isFlying": Boolean,
    "isPoisonous": Boolean,
}

If it is not an insect, return the following schema:
  
  {
      "isInsect": Boolean,
      "message": "This is not an insect"
  }
  
If you are not sure, return the following schema:
    
    {
        "isInsect": Boolean,
        "message": "I am not sure"
    }
    
always return a response following the correct schema
"""

FILE_ANALYZE_PROMPT = os.getenv("FILE_ANALYZE_PROMPT", DEFAULT_PROMPT)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

file_router = APIRouter()


@file_router.post(
    "/analyze",
    response_model=BaseResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not allowed",
        )
    if file.content_length > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size too large",
        )
    path = save_file(file)
    try:
        res = gemini.analyze_image(path, FILE_ANALYZE_PROMPT)
        delete_file(path)
        return {"data": res}
    except Exception as e:
        delete_file(path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
