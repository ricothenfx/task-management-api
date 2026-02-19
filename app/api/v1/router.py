from fastapi import APIRouter
from app.api.v1.endpoints import task, auth

api_router = APIRouter()

api_router.include_router(task.router)
api_router.include_router(auth.router)