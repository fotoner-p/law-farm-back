from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

DATABASE_URL = f'mysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}/{settings.MYSQL_DB}?charset=utf8mb4'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
