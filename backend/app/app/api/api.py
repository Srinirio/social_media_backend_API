from fastapi import APIRouter
from api.endpoints import login,registration_api,profile,post_api,chat_api

api_router = APIRouter()

api_router.include_router(login.router, tags=["Login"])
api_router.include_router(registration_api.router, tags=["Registration"])
api_router.include_router(profile.router, tags=["Profile"])
api_router.include_router(post_api.router, tags=["Posts"])
api_router.include_router(chat_api.router, tags=["Chat"])