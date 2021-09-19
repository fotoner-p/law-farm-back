from typing import Any

from sqlalchemy.orm import Session

import models
import schemas
from core.security import get_password_hash, verify_password


def get(db: Session, id: Any):
    return db.query(models.User).filter(models.User.id == id).first()


def get_multi(db: Session, *, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_by_email(db: Session, *, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create(db: Session, *, user_in: schemas.UserCreate):
    db_obj = models.User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        is_active=True,
        is_superuser=False,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return db_obj


def is_active(user: models.User):
    return user.is_active


def is_superuser(user: models.User):
    return user.is_superuser


def authenticate(db: Session, *, email: str, password: str):
    user = get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
