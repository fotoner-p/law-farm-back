import datetime

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

# 나중에 방법 알고 쪼개기


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(99), unique=True, index=True, nullable=False)
    hashed_password = Column(String(99), nullable=False)
    username = Column(String(30), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    bookmarks = relationship("Bookmark", back_populates="owner")
    view_logs = relationship("ViewLog", back_populates="owner")


class Bookmark(Base):
    __tablename__ = 'bookmarks'

    id = Column(Integer, primary_key=True, index=True)
    content_type = Column(String(15), nullable=False)
    content_key = Column(String(99), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="bookmarks")


class ViewLog(Base):
    __tablename__ = 'view_logs'

    id = Column(Integer, primary_key=True, index=True)
    content_type = Column(String(15), nullable=False)
    content_key = Column(String(99), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="view_logs")