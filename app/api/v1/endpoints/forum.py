from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

import app.api.dependency as deps
from app import crud, models, schemas

router = APIRouter(
    prefix="/forums",
    tags=["forums"],
    responses={404: {"description": "Not found"}},
)


def raw_forum_reform(raw):
    row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}
    res_forum = {**row2dict(raw["Forum"]), "user": raw["User"]}

    return res_forum


@router.get("/", response_model=schemas.ForumPage)
def read_forums_multi(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    forums = crud.forum.get_multi(db, skip=skip, limit=limit)
    parsed_forums = [raw_forum_reform(forum) for forum in forums]

    count = crud.forum.get_count(db)

    result = {
        "data": parsed_forums,
        "count": count,
        "size": len(parsed_forums),
        "skip": skip,
        "limit": limit
    }

    return result


@router.post("/", response_model=schemas.Forum)
def post_forum(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        title: str = Body(..., min_length=1),
        forum_type: str = Body(..., regex="(교통사고|층간소음|창업|퇴직금|가족|학교폭력)"),
        main: str = Body(..., min_length=1),
        secret: bool = Body(False)
) -> Any:
    forum_in = schemas.ForumCreate(title=title, forum_type=forum_type, main=main, secret=secret)
    forum = crud.forum.create_with_owner(db, obj_in=forum_in, owner_id=current_user.id)

    return forum


@router.put("/@{forum_id}", response_model=schemas.Forum)
def update_forum(
        *,
        db: Session = Depends(deps.get_db),
        forum_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
        title: str = Body(None, min_length=1),
        forum_type: str = Body(None, regex="(교통사고|층간소음|창업|퇴직금|가족|학교폭력)"),
        main: str = Body(None, min_length=1),
) -> Any:
    forum = crud.forum.get(db, obj_id=forum_id)

    if not forum:
        raise HTTPException(status_code=404, detail="Item not found")

    if crud.user.is_active(current_user) and (forum.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    forum_in = schemas.ForumUpdate()

    if title is not None:
        forum_in.title = title
    if forum_type is not None:
        forum_in.forum_type = forum_type
    if main is not None:
        forum_in.main = main

    forum = crud.forum.update(db, db_obj=forum, obj_in=forum_in)

    return forum


@router.delete("/@{forum_id}", response_model=schemas.Forum)
def delete_forum(
        *,
        forum_id: int,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:

    forum = crud.forum.get(db, obj_id=forum_id)

    if not forum:
        raise HTTPException(status_code=404, detail="Item not found")
    if crud.user.is_active(current_user) and (forum.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    forum = crud.forum.remove(db, obj_id=forum_id)

    return forum


@router.get("/@{forum_id}", response_model=schemas.ForumUser)
def read_forum(
        forum_id: int,
        db: Session = Depends(deps.get_db)
) -> Any:
    forum = crud.forum.get(db, obj_id=forum_id)
    if not forum:
        raise HTTPException(status_code=404, detail="Item not found")

    res_forum = raw_forum_reform(forum)

    return res_forum

