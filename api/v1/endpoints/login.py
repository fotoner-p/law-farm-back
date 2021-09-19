from typing import Any
from datetime import datetime, timedelta

from fastapi import status, HTTPException, Depends, APIRouter, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.config import settings
from core.security import create_access_token

import api.dependency as deps
import schemas
import crud

router = APIRouter(
    prefix="/login",
    tags=["login"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
