from typing import Any

from sqlalchemy.orm import Session

import models
import schemas
from core.security import get_password_hash, verify_password


def exist(db: Session, *, user: models.User, bookmark: schemas.BookmarkCreate):
    bookmark = db.query(models.Bookmark).filter(
        models.Bookmark.owner_id == user.id and
        models.Bookmark.content_type == bookmark.content_type and
        models.Bookmark.content_key == bookmark.content_key
    ).first()

    return True if bookmark else False


def get_by_user(db: Session, *, bookmark_id: int, user: models.User):
    bookmark = db.query(models.Bookmark).filter(
        models.Bookmark.owner_id == user.id and
        models.Bookmark.id == bookmark_id
    ).first()

    return bookmark


def get_multi_by_user(db: Session, *, user: models.User):
    return db.query(models.Bookmark).filter(models.Bookmark.owner_id == user.id).all()


def create_user_bookmark(db: Session, *, user: models.User, bookmark: schemas.BookmarkCreate):
    db_obj = models.Bookmark(
        content_type=bookmark.content_type,
        content_key=bookmark.content_key,
        owner_id=user.id
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return db_obj


def remove_bookmark(db: Session, *, bookmark_id: int):
    obj = db.query(models.Bookmark).get(bookmark_id)

    db.delete(obj)
    db.commit()

    return obj
