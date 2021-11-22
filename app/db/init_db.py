# from sqlalchemy.orm import Session
#
# from core.config import settings
# from db import base
from app.db.session import engine
from app.models import models


def init_db() -> None:
    models.Base.metadata.create_all(bind=engine)
