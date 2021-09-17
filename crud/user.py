from sqlalchemy.orm import Session

import models, schemas


def get_multi(db: Session, *, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

