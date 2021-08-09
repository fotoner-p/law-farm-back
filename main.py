from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from routers import ml, law, auth, user

app = FastAPI()
origins = [
    'http://localhost:3000',
]

api_router = APIRouter()
routers = [
    ml, law, auth, user
]

for route in routers:
    app.include_router(route.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
