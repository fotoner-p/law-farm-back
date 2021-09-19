from typing import Any, List
from datetime import datetime, timedelta

from fastapi import status, HTTPException, Depends, APIRouter, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models
from core.config import settings
from core.security import create_access_token

import api.dependency as deps
import schemas
import crud

router = APIRouter(
    prefix="/logs",
    tags=["logs"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/me", response_model=List[schemas.Log])
def read_bookmarks(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    logs = crud.log.get_multi_by_user(db, user=current_user)
    return logs
