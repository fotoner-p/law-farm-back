from typing import Any, List

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

import app.api.dependency as deps
from app import crud, models, schemas

router = APIRouter(
    prefix="/bookmarks",
    tags=["bookmarks"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/me", response_model=schemas.BookmarkPage)
def read_bookmarks(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    bookmarks = crud.bookmark.get_multi_by_owner(db, skip=skip, limit=limit, owner=current_user)
    count = crud.bookmark.get_count_by_owner(db, owner=current_user)
    result = {
        "data": bookmarks,
        "count": count,
        "size": len(bookmarks),
        "skip": skip,
        "limit": limit
    }

    return result


@router.get("/article/@{key}", response_model=schemas.Bookmark)
def get_bookmark_exist(
        key: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user_or_none)
) -> Any:
    bookmark = crud.bookmark.get_with_owner(db, content_key=key, content_type="article", owner=current_user)

    if not bookmark:
        raise HTTPException(
            status_code=404,
            detail="This bookmark is not exists."
        )

    return bookmark


@router.post("/article/@{key}", response_model=schemas.Bookmark)
def add_bookmark(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        key: str
) -> Any:
    bookmark_in = schemas.BookmarkCreate(content_type="article", content_key=key)

    if crud.bookmark.is_exist(db, owner=current_user, bookmark=bookmark_in):
        raise HTTPException(
            status_code=400,
            detail="This bookmark already exists."
        )
    bookmark = crud.bookmark.create_with_owner(db, owner_id=current_user.id, obj_in=bookmark_in)

    return bookmark


@router.delete("/article/@{key}", response_model=schemas.Bookmark)
def delete_bookmark(
        *,
        db: Session = Depends(deps.get_db),
        key: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    bookmark = crud.bookmark.get_with_owner(db, content_key=key, content_type="article", owner=current_user)

    if not bookmark:
        raise HTTPException(status_code=404, detail="Item not found")

    item = crud.bookmark.remove(db=db, obj_id=bookmark.id)
    return item
