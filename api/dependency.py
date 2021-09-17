from fastapi.security import OAuth2PasswordBearer

from core.config import settings
from db.session import SessionLocal


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PATH}/login/access-token"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
