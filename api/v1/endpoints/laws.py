from typing import Optional

from fastapi import APIRouter, Depends, HTTPException


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
def get_article(key: str):
    return reform_result(key, article_dict)


@router.get("/paragraph/@{key}")
def get_paragraph(key: str):
    return reform_result(key, paragraph_dict)


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

