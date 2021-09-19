from sqlalchemy.orm import Session

import models
import schemas


def get_by_user(db: Session, *, view_id: int, user: models.User):
    bookmark = db.query(models.ViewLog).filter(
        models.ViewLog.owner_id == user.id and
        models.ViewLog.id == view_id
    ).first()

    return bookmark


def get_multi_by_user(db: Session, *, user: models.User):
    return db.query(models.ViewLog).filter(models.ViewLog.owner_id == user.id).all()


def create_user_log(db: Session, *, user: models.User, view: schemas.LogCreate):
    db_obj = models.ViewLog(
        content_type=view.content_type,
        content_key=view.content_key,
        owner_id=user.id
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return db_obj
