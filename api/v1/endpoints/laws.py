from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

import crud.log
import models
import schemas
from lib.data_utils import get_paragraph_dict, get_article_dict
import api.dependency as deps


router = APIRouter(
    prefix="/laws",
    tags=["laws"],
    responses={404: {"description": "Not found"}},
)

paragraph_dict: dict = get_paragraph_dict()
article_dict: dict = get_article_dict()
article_names = sorted([key for key in article_dict.keys()])


def reform_result(key: str, info_dict: dict):
    try:
        return {
            "result": info_dict[key],
            "detail": "ok"
        }
    except:
        raise HTTPException(status_code=404, detail="Item not found")


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
            content_type='article'
        )
        res = crud.log.create_user_log(db, user=current_user, view=log)
        print(res)
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
            content_type='paragraph'
        )
        res = crud.log.create_user_log(db, user=current_user, view=log)
        print(res)
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

