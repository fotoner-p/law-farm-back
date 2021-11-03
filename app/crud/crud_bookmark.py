from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import models
from app.crud.base import CRUDBase
from app.models import Bookmark
from app.schemas.bookmark import BookmarkCreate, BookmarkUpdate


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
        self, db: Session, *, content_key: str, content_type: str, owner: models.User
    ) -> Bookmark:
        return db.query(self.model).filter(
            self.model.owner_id == owner.id and
            self.model.content_key == content_key and
            self.model.content_type == content_type
        ).first()

    def get_multi_by_owner(
        self, db: Session, *, skip: int = 0, limit: int = 100, owner: models.User
    ) -> List[Bookmark]:
        return (
            db.query(self.model)
            .filter(self.model.owner_id == owner.id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def is_exist(
        self, db: Session, *, owner: models.User, bookmark: BookmarkCreate
    ) -> bool:
        result = db.query(self.model).filter(
            self.model.owner_id == owner.id and
            self.model.content_type == bookmark.content_type and
            self.model.content_key == bookmark.content_key
        ).first()

        return True if result else False

    def get_count_by_owner(self, db: Session, *, owner: models.User):
        return db.query(self.model).filter(self.model.owner_id == owner.id).count()


bookmark = CRUDBookmark(Bookmark)
