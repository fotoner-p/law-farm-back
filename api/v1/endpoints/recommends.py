from fastapi import APIRouter, Query, HTTPException
from typing import Optional, Any

from lib.DocumentCore import Core
from lib.data_utils import get_paragraph_dict, get_article_dict

router = APIRouter(
    prefix="/recommends",
    tags=["recommends"],
    responses={404: {"description": "Not found"}},
)

nlp_core = Core()
paragraph_dict: dict = get_paragraph_dict()
article_dict: dict = get_article_dict()

SIZE_OPTION_DEFAULT = 25


def reform_result(data: dict, info_dict: dict):
    return {
        "result": [
            {
                "name": val[0],
                "weight": val[1],
                "about": info_dict[val[0]]
            } for val in data
        ],
        "detail": "ok"
    }


def query_wrapper(*, callback, query: str, size: int):
    try:
        return callback(query, size)
    except:
        raise HTTPException(status_code=404, detail="Item not found")


@router.get("/search")
async def search_query(
        query: str,
        target: str = Query("article", regex="(article|paragraph)"),
        size: Optional[int] = SIZE_OPTION_DEFAULT
) -> Any:
    result = query_wrapper(
        callback=nlp_core.article.search if target == "article" else nlp_core.paragraph.search,
        query=query,
        size=size
    )
    return reform_result(result, article_dict if target == "article" else paragraph_dict)


@router.get("/article")
async def relate_article(
        key: str,
        size: Optional[int] = SIZE_OPTION_DEFAULT
) -> Any:
    result = query_wrapper(callback=nlp_core.article.article, query=key, size=size)
    return reform_result(result, article_dict)


@router.get("/paragraph")
async def relate_paragraph(
        key: str,
        size: Optional[int] = SIZE_OPTION_DEFAULT
) -> Any:
    result = query_wrapper(callback=nlp_core.paragraph.paragraph, query=key, size=size)
    return reform_result(result, paragraph_dict)


@router.get("/article/paragraph")
async def to_paragraph(
        key: str,
        size: Optional[int] = SIZE_OPTION_DEFAULT
) -> Any:
    result = query_wrapper(callback=nlp_core.article.paragraph, query=key, size=size)
    return reform_result(result, paragraph_dict)


@router.get("/paragraph/article")
async def to_article(
        key: str,
        size: Optional[int] = SIZE_OPTION_DEFAULT
) -> Any:
    result = query_wrapper(callback=nlp_core.paragraph.article, query=key, size=size)
    return reform_result(result, article_dict)
