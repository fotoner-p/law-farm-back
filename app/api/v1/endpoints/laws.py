from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.lib.data_utils import get_paragraph_dict, get_article_dict, get_statues_dict
import app.api.dependency as deps


router = APIRouter(
    prefix="/laws",
    tags=["laws"],
    responses={404: {"description": "Not found"}},
)

paragraph_dict: dict = get_paragraph_dict()
article_dict: dict = get_article_dict()
statute_dict: dict = get_statues_dict()
article_names = sorted([key for key in article_dict.keys()])
statute_names = sorted([key for key in statute_dict.keys()])


def reform_result(key: str, info_dict: dict):
    try:
        curResult = info_dict[key]
        if curResult["paragraphs"]:
            paragraphs = sorted(curResult["paragraphs"], key=lambda x: len(x["paragraph"]))
            curResult["paragraphs"] = paragraphs

        return {
            "result": curResult,
            "detail": "ok"
        }
    except:
        raise HTTPException(status_code=404, detail="Item not found")


@router.get("/statute/types")
def get_statute_types():
    return {
        "result": statute_names,
        "detail": "ok"
    }


@router.get("/statute/@{key}")
def get_statute(
        key: str,
        skip: int = 0,
        limit: int = 100,
):
    # print(limit)
    try:
        statute = statute_dict[key]
    except:
        raise HTTPException(status_code=404, detail="Item not found")

    result = [
        {
            "fullname": article["fullname"],
            "article": article["article"],
            "text": article["text"] if article["text"] else "",
            "statute": article["statute"],
            "count": len(article["paragraphs"]) if "paragraphs" in article.keys() else 1
        } for article in statute["articles"]
    ]
    result.sort(key=lambda x: x["article"])
    result.sort(key=lambda x: len(x["article"]))
    count = len(result)

    result = result[skip: skip + limit]

    return {
        "result": result,
        "detail": "ok",
        "count": count,
        "size": len(result),
        "skip": skip,
        "limit": limit,
    }


@router.get("/article/@{key}")
def get_article(
        key: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user_or_none)
):
    """
    jwt 토큰이 존재할 경우 해당 계정 토큰을 기준으로 로깅 처리가 된다<br>
    (토큰이 존재하지 않을경우 결과만 반환)
    """
    article = reform_result(key, article_dict)
    if current_user:
        log = schemas.LogCreate(
            content_key=key,
            content_type='article',
            text=article_dict[key]["text"][:99]
        )
        res = crud.log.create_with_owner(db, obj_in=log, owner_id=current_user.id)
    return article


@router.get("/paragraph/@{key}")
def get_paragraph(
        key: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user_or_none)
):
    """
    jwt 토큰이 존재할 경우 해당 계정 토큰을 기준으로 로깅 처리가 된다 <br>
    (토큰이 존재하지 않을경우 결과만 반환)
    """
    paragraph = reform_result(key, paragraph_dict)
    if current_user:
        log = schemas.LogCreate(
            content_key=key,
            content_type='paragraph',
            text=paragraph_dict[key]["text"]
        )
        res = crud.log.create_with_owner(db, obj_in=log, owner_id=current_user.id)
    return paragraph


@router.get("/keyword/dict")
async def match_keyword(
    query: str,
    size: Optional[int] = 10
):
    result = []

    for name in article_names:
        if query in name:
            result.append(name)

        if len(result) == size:
            break

    return {
        "result": result
    }

