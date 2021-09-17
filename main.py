from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from api.v1.api import api_router
from db.init_db import init_db

init_db()

app = FastAPI(
    title=settings.API_SERVER_NAME, openapi_url=f"{settings.API_V1_PATH}/openapi.json"
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_PATH)
