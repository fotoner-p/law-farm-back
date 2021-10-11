from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import models
from app.crud.base import CRUDBase
from app.models import ViewLog
from app.schemas.log import LogCreate, LogUpdate


class CRUDLog(CRUDBase[ViewLog, LogCreate, LogUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: LogCreate, owner_id: int
    ) -> ViewLog:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def get_with_owner(
        self, db: Session, *, log_id: int, owner: models.User
    ) -> ViewLog:
        return db.query(self.model).filter(
            self.model.owner_id == owner.id and
            self.model.id == log_id
        ).first()

    def get_multi_by_owner(
        self, db: Session, *, owner: models.User
    ) -> List[ViewLog]:
        return (
            db.query(self.model)
            .filter(self.model.owner_id == owner.id)
            .order_by(self.model.created_at.desc())
            .all()
        )

    def get_multi_by_user_id(
        self, db: Session, *, user_id: int
    ) -> List[ViewLog]:
        return (
            db.query(self.model)
            .filter(self.model.owner_id == user_id)
            .order_by(self.model.created_at.desc())
            .all()
        )

    def get_multi_by_email(
        self, db: Session, *, email: str
    ) -> List[ViewLog]:
        return (
            db.query(self.model)
            .join(models.User)
            .filter(models.User.email == email)
            .order_by(self.model.created_at.desc())
            .all()
        )

    def get_count_by_user_id(
        self, db: Session, *, user_id: int
    ):
        return db.query(self.model).filter(self.model.owner_id == user_id).count()

    def get_count_by_email(
        self, db: Session, *, email: str
    ):
        return db.query(self.model).join(models.User).filter(models.User.email == email).count()



log = CRUDLog(ViewLog)
