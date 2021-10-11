from typing import Union, Dict, Any

from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models import Forum, User
from app.schemas.forum import ForumCreate, ForumUpdate
from app.lib.Parse import parse_md


class CRUDForum(CRUDBase[Forum, ForumCreate, ForumUpdate]):
    def get(self, db: Session, obj_id: Any) -> Any:
        return db.query(self.model, User).join(User, User.id == self.model.owner_id).filter(self.model.id == obj_id).first()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> Any:
        return db.query(self.model, User).join(User, User.id == self.model.owner_id).order_by(self.model.created_at.desc()).offset(skip).limit(limit).all()

    def create_with_owner(self, db: Session, *, obj_in: ForumCreate, owner_id: int) -> Forum:

        obj_in_data = jsonable_encoder(obj_in)
        parsed_main = parse_md(obj_in.main)

        db_obj = self.model(**obj_in_data, parse_short_main=parsed_main[:100], owner_id=owner_id)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(
            self, db: Session, *, db_obj: Forum, obj_in: Union[ForumUpdate, Dict[str, Any]]
    ) -> Forum:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if update_data.get("main"):
            parsed_main = parse_md(update_data["main"])
            update_data["parse_short_main"] = parsed_main

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_count(self, db: Session) -> Any:
        return db.query(self.model.id).count()


forum = CRUDForum(Forum)

