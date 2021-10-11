from fastapi import APIRouter

from app.api.v1.endpoints import users, laws, recommends, login, bookmarks, logs, forum

api_router = APIRouter()
api_router.include_router(laws.router)
api_router.include_router(users.router)
api_router.include_router(login.router)
api_router.include_router(recommends.router)
api_router.include_router(bookmarks.router)
api_router.include_router(logs.router)
api_router.include_router(forum.router)