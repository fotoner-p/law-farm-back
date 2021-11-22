from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Body, Query
from sqlalchemy.orm import Session

import app.api.dependency as deps
from app import crud, models, schemas

router = APIRouter(
    prefix="/forums",
    tags=["forums"],
    responses={404: {"description": "Not found"}},
)


row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}


def raw_forum_reform(raw):
    res_forum = {**row2dict(raw["Forum"]), "user": raw["User"]}

    return res_forum


@router.get("", response_model=schemas.ForumPage)
def read_forums_multi(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        forum_type: Optional[str] = Query(None, regex="(전체|교통사고|층간소음|창업|퇴직금|가족|학교폭력|기타)"),
        sort_type: Optional[str] = Query(None, regex="(date|like|view|comment)")
) -> Any:
    forums = crud.forum.get_multi_options(db, skip=skip, limit=limit, forum_type=forum_type, sort_type=sort_type)
    parsed_forums = [raw_forum_reform(forum) for forum in forums]

    count = crud.forum.get_option_count(db, forum_type=forum_type, sort_type=sort_type)

    result = {
        "data": parsed_forums,
        "count": count,
        "size": len(parsed_forums),
        "skip": skip,
        "limit": limit
    }

    return result


@router.post("", response_model=schemas.Forum)
def post_forum(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        title: str = Body(..., min_length=1),
        forum_type: str = Body(..., regex="(교통사고|층간소음|창업|퇴직금|가족|학교폭력|기타)"),
        main: str = Body(..., min_length=1),
        secret: bool = Body(False)
) -> Any:
    forum_in = schemas.ForumCreate(title=title, forum_type=forum_type, main=main, secret=secret)
    forum = crud.forum.create_with_owner(db, obj_in=forum_in, owner_id=current_user.id)

    return forum


@router.get("/liked", response_model=schemas.ForumPage)
def read_forums_multi(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    forums = crud.forum.get_multi_liked(db, skip=skip, limit=limit, owner_id=current_user.id)
    parsed_forums = [raw_forum_reform(forum) for forum in forums]

    count = crud.forum.get_liked_count(db, owner_id=current_user.id)

    result = {
        "data": parsed_forums,
        "count": count,
        "size": len(parsed_forums),
        "skip": skip,
        "limit": limit
    }

    return result


@router.put("/@{forum_id}", response_model=schemas.Forum)
def update_forum(
        *,
        db: Session = Depends(deps.get_db),
        forum_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
        title: str = Body(None, min_length=1),
        forum_type: str = Body(None, regex="(교통사고|층간소음|창업|퇴직금|가족|학교폭력|기타)"),
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
    if crud.user.is_active(current_user) and (forum["Forum"].owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    forum = crud.forum.remove(db, obj_id=forum_id)

    return forum


@router.get("/@{forum_id}", response_model=schemas.ForumUser)
def read_forum(
        forum_id: int,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    forum = crud.forum.get(db, obj_id=forum_id)
    if not forum:
        raise HTTPException(status_code=404, detail="Item not found")

    res = crud.forumCount.get_with_owner_and_forum(db, forum_id=forum_id, owner_id=current_user.id)

    if not res:
        count = schemas.ForumCountCreate(
            owner_id=current_user.id,
            forum_id=forum_id
        )
        crud.forumCount.create(db, obj_in=count)
        crud.forum.update_count(db, forum_id=forum_id)

    res_forum = raw_forum_reform(forum)

    return res_forum


@router.get("/@{forum_id}/like", response_model=schemas.ForumLike)
def read_forum_like(
        forum_id: int,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    return crud.forumLike.get_with_owner_and_forum(db, forum_id=forum_id, owner_id=current_user.id)


@router.post("/@{forum_id}/like", response_model=schemas.ForumLike)
def add_forum_like(
        forum_id: int,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    if crud.forumLike.get_with_owner_and_forum(db, forum_id=forum_id, owner_id=current_user.id):
        raise HTTPException(
            status_code=400,
            detail="This bookmark already exists."
        )

    like = schemas.ForumLikeCreate(
        owner_id=current_user.id,
        forum_id=forum_id
    )

    res = crud.forumLike.create(db, obj_in=like)
    crud.forum.update_like_add(db, forum_id=forum_id)
    return res


@router.delete("/@{forum_id}/like", response_model=schemas.ForumLike)
def remove_forum_like(
        forum_id: int,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    if not crud.forumLike.get_with_owner_and_forum(db, forum_id=forum_id, owner_id=current_user.id):
        raise HTTPException(status_code=404, detail="Item not found")

    like = crud.forumLike.remove_with_owner_and_forum(db, forum_id=forum_id, owner_id=current_user.id)
    crud.forum.update_like_delete(db, forum_id=forum_id)
    return like


@router.get("/@{forum_id}/comment", response_model=schemas.ForumAnswerPage, dependencies=[Depends(deps.get_current_active_user)])
def get_forum_comment(
        forum_id: int,
        db: Session = Depends(deps.get_db),
) -> Any:
    answers = crud.forumAnswer.get_multi_by_forum(db, forum_id=forum_id)
    print(answers)
    res_answers = [{**row2dict(answer["ForumAnswer"]), "user": answer["User"]} for answer in answers]

    return {
        "data": res_answers
    }


@router.post("/@{forum_id}/comment", response_model=schemas.ForumAnswer)
def create_forum_comment(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        forum_id: int,
        main: str = Body(..., min_length=1, embed=True),
) -> Any:
    forum_in = schemas.ForumAnswerCreate(main=main, forum_id=forum_id, owner_id=current_user.id)
    crud.forum.update_comment_add(db, forum_id=forum_id)
    return crud.forumAnswer.create(db, obj_in=forum_in)


@router.delete("/@{forum_id}/comment/@{comment_id}", response_model=schemas.ForumAnswer)
def delete_forum_comment(
        forum_id: int,
        comment_id: int,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    res = crud.forumAnswer.remove_with_owner_and_id(db, obj_id=comment_id, forum_id=forum_id, owner_id=current_user.id)

    if not res:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        crud.forum.update_comment_delete(db, forum_id=forum_id)
        return res

