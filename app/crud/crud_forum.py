from typing import Union, Dict, Any

from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models import Forum
from app.schemas.forum import ForumCreate, ForumUpdate
from app.lib.Parse import parse_md


class CRUDForum(CRUDBase[Forum, ForumCreate, ForumUpdate]):
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


forum = CRUDForum(Forum)

