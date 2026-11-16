from fastapi import APIRouter

from .download_router import router as download_router

api_v1_router = APIRouter()
api_v1_router.include_router(download_router)
