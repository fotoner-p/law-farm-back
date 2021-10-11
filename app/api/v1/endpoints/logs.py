from typing import Any, List

from pydantic.networks import EmailStr
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

import app.api.dependency as deps
from app import crud, models, schemas

router = APIRouter(
    prefix="/logs",
    tags=["logs"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/@{user_id}", response_model=List[schemas.Log], dependencies=[Depends(deps.get_current_active_superuser)])
def admin_read_bookmarks_by_id(
        user_id: int,
        db: Session = Depends(deps.get_db),
) -> Any:
    logs = crud.log.get_multi_by_user_id(db, user_id=user_id)
    return logs


@router.get("/email", response_model=List[schemas.Log], dependencies=[Depends(deps.get_current_active_superuser)])
def admin_read_bookmarks_by_email(
        email: EmailStr,
        db: Session = Depends(deps.get_db),
) -> Any:
    logs = crud.log.get_multi_by_email(db, email=str(email))
    return logs


@router.get("/me", response_model=List[schemas.Log])
def read_bookmarks(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    logs = crud.log.get_multi_by_owner(db, owner=current_user)
    return logs

