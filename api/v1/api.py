
from fastapi import APIRouter

from api.v1.endpoints import users, laws, recommends, login, bookmarks

api_router = APIRouter()
api_router.include_router(laws.router)
api_router.include_router(users.router)
api_router.include_router(login.router)
api_router.include_router(recommends.router)
api_router.include_router(bookmarks.router)

