from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

from routers import ml, law, auth, user

app = FastAPI(
    title=settings.API_SERVER_NAME, openapi_url=f"{settings.API_V1_PATH}/openapi.json"
)

api_router = APIRouter()
routers = [
    ml,
    law,
    auth,
    user
]

for route in routers:
    api_router.include_router(route.router)


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_PATH)
