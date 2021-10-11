from typing import Any, List
from pydantic.networks import EmailStr

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import app.api.dependency as deps
from app import crud, schemas, models

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.UserPage, dependencies=[Depends(deps.get_current_active_superuser)])
def admin_read_users(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    count = crud.user.get_count(db)

    result = {
        "data": users,
        "count": count,
        "size": len(users),
        "skip": skip,
        "limit": limit
    }

    return result


@router.post("/", response_model=schemas.User)
def create_user(
        *,
        db: Session = Depends(deps.get_db),
        email: EmailStr = Body(...),
        password: str = Body(..., min_length=8, max_length=72),
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


@router.get("/me", response_model=schemas.User)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=schemas.User)
def update_user_me(
        *,
        db: Session = Depends(deps.get_db),
        password: str = Body(None, min_length=10, max_length=72),
        username: str = Body(None, min_length=3, max_length=20),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)

    if password is not None:
        user_in.password = password
    if username is not None:
        user_in.username = username
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.delete("/me", response_model=schemas.User)
def delete_user_me(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    user = crud.user.remove(db, current_user.id)
    return user
