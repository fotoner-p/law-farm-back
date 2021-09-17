from typing import Any, List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, HTTPException


from api.dependency import get_db

import crud, models, schemas

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.User])
def read_users(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        # current_user: models.User = Depends() << deps.get_current_active_superuser
):
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users
