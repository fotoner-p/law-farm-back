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
    prefix="/bookmarks",
    tags=["bookmarks"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/me", response_model=List[schemas.Bookmark])
def read_bookmarks(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    bookmarks = crud.bookmark.get_multi_by_owner(db, owner=current_user)
    return bookmarks


@router.post("/me", response_model=schemas.Bookmark)
def add_bookmark(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        bookmark_in: schemas.BookmarkCreate
) -> Any:
    if crud.bookmark.is_exist(db, user=current_user, bookmark=bookmark_in):
        raise HTTPException(
            status_code=400,
            detail="This bookmark already exists."
        )
    bookmark = crud.bookmark.create_with_owner(db, owner_id=current_user.id, obj_in=bookmark_in)

    return bookmark


@router.delete("/me", response_model=schemas.Bookmark)
def delete_bookmark(
        *,
        db: Session = Depends(deps.get_db),
        bookmark_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
):
    bookmark = crud.bookmark.get_with_owner(db, bookmark_id=bookmark_id, owner=current_user)

    if not bookmark:
        raise HTTPException(status_code=404, detail="Item not found")

    item = crud.bookmark.remove(db=db, obj_id=bookmark_id)
    return item
