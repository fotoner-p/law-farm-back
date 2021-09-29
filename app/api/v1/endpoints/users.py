from typing import Any, List
from pydantic.networks import EmailStr

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

import app.api.dependency as deps
from app import crud, schemas

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.User], dependencies=[Depends(deps.get_current_active_superuser)])
def read_users(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
        *,
        db: Session = Depends(deps.get_db),
        email: EmailStr = Body(...),
        password: str = Body(..., min_length=10, max_length=72),
        username: str = Body(..., min_length=3, max_length=20),
) -> Any:
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system."
        )

    user_in = schemas.UserCreate(email=email, password=password, username=username)
    user = crud.user.create(db, obj_in=user_in)

    return user
