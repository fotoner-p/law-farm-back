from typing import Optional

from fastapi import APIRouter, Query
from lib.DocumentCore import Core
from lib.data_utils import get_paragraph_dict, get_article_dict

router = APIRouter(
    prefix="/law",
    tags=["law"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

paragraph_dict: dict = get_paragraph_dict()
article_dict: dict = get_article_dict()
article_names = sorted([key for key in article_dict.keys()])


@router.get("/article")
async def get_article(
        key: str,
):
    try:
        return {
            "result": article_dict[key],
            "message": "ok"
        }
    except:
        return {
            "message": "does not exist"
        }


@router.get("/paragraph")
async def get_paragraph(
        key: str,
):
    try:
        return {
            "result": paragraph_dict[key],
            "message": "ok"
        }
    except:
        return {
            "message": "does not exist"
        }



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
