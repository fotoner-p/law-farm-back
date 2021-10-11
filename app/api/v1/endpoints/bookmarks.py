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


@router.post("/me", response_model=schemas.Bookmark)
def add_bookmark(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        bookmark_in: schemas.BookmarkCreate
) -> Any:
    if crud.bookmark.is_exist(db, owner=current_user, bookmark=bookmark_in):
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
) -> Any:
    bookmark = crud.bookmark.get_with_owner(db, bookmark_id=bookmark_id, owner=current_user)

    if not bookmark:
        raise HTTPException(status_code=404, detail="Item not found")

    item = crud.bookmark.remove(db=db, obj_id=bookmark_id)
    return item
