from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from schemas import DB_ENV

DATABASE_URL = f'mysql://{DB_ENV["user"]}:{DB_ENV["password"]}@{DB_ENV["host"]}/{DB_ENV["db"]}'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker()