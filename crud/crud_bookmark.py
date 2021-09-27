from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import models
from crud.base import CRUDBase
from models import Bookmark
from schemas.bookmark import BookmarkCreate, BookmarkUpdate


class CRUDBookmark(CRUDBase[Bookmark, BookmarkCreate, BookmarkUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: BookmarkCreate, owner_id: int
    ) -> Bookmark:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def get_with_owner(
        self, db: Session, *, bookmark_id: int, owner: models.User
    ) -> Bookmark:
        return db.query(self.model).filter(
            self.model.owner_id == owner.id and
            self.model.id == bookmark_id
        ).first()

    def get_multi_by_owner(
        self, db: Session, *, owner: models.User
    ) -> List[Bookmark]:
        return (
            db.query(self.model)
            .filter(self.model.owner_id == owner.id)
            .order_by(self.model.created_at.desc())
            .all()
        )

    def is_exist(
        self, db: Session, *, user: models.User, bookmark: BookmarkCreate
    ) -> bool:
        result = db.query(self.model).filter(
            self.model.owner_id == user.id and
            self.model.content_type == bookmark.content_type and
            self.model.content_key == bookmark.content_key
        ).first()

        return True if result else False


bookmark = CRUDBookmark(Bookmark)
