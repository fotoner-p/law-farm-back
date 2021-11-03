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


@router.get("/@{user_id}", response_model=schemas.LogPage, dependencies=[Depends(deps.get_current_active_superuser)])
def admin_read_logs_by_id(
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(deps.get_db),
) -> Any:
    logs = crud.log.get_multi_by_user_id(db, user_id=user_id, skip=skip, limit=limit)
    count = crud.log.get_count_by_user_id(db, user_id=user_id)

    result = {
        "data": logs,
        "count": count,
        "size": len(logs),
        "skip": skip,
        "limit": limit
    }

    return result


@router.get("/email", response_model=schemas.LogPage, dependencies=[Depends(deps.get_current_active_superuser)])
def admin_read_logs_by_email(
        email: EmailStr,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(deps.get_db),
) -> Any:
    logs = crud.log.get_multi_by_email(db, email=str(email), skip=skip, limit=limit)
    count = crud.log.get_count_by_email(db, email=str(email))

    result = {
        "data": logs,
        "count": count,
        "size": len(logs),
        "skip": skip,
        "limit": limit
    }

    return result


@router.get("/me", response_model=schemas.LogPage)
def read_logs(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    logs = crud.log.get_multi_by_owner(db, owner=current_user, skip=skip, limit=limit)
    count = crud.log.get_count_by_user_id(db, user_id=current_user.id)

    result = {
        "data": logs,
        "count": count,
        "size": len(logs),
        "skip": skip,
        "limit": limit
    }

    return result

