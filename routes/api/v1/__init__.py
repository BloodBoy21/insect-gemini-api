from fastapi import APIRouter
from routes.api.v1.file import file_router

api_v1_router = APIRouter()

api_v1_router.include_router(file_router, prefix="/file", tags=["file"])
