from typing import Optional

from fastapi import APIRouter, Query
from lib.DocumentCore import Core
from lib.data_utils import get_paragraph_dict, get_article_dict

router = APIRouter(
    prefix="/ml",
    tags=["ml"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

nlp_core = Core()
paragraph_dict: dict = get_paragraph_dict()
article_dict: dict = get_article_dict()


@router.get("/search")
async def read_all_users(
    query: str,
    target: str = Query("article", regex="(article|paragraph)"),
    size: Optional[int] = 25
):
    try:
        if target == "article":
            result = nlp_core.search_article(query, size)
        else:
            result = nlp_core.search_paragraph(query, size)
    except:
        return {
          "result": [],
          "message": "does not exist"
        }

    reform = {
        "result": [
            {
                "name": val[0],
                "weight": val[1],
                "about": paragraph_dict[val[0]] if target == "paragraph" else article_dict[val[0]]
            } for val in result
        ],
        "message": "ok"
    }

    return reform


@router.get("/article")
async def relate_article(
    key: str,
    size: Optional[int] = 25
):
    try:
        result = nlp_core.relate_article(key, size)
        reform = {
            "result": [
                {
                    "name": val[0],
                    "weight": val[1],
                    "about": article_dict[val[0]]
                } for val in result
            ],
            "message": "ok"
        }

    except:
        reform = {
          "result": [],
          "message": "does not exist"
        }

    return reform

@router.get("/paragraph")
async def relate_paragraph(
    key: str,
    size: Optional[int] = 25
):
    try:
        result = nlp_core.relate_paragraph(key, size)
        reform = {
            "result": [
                {
                    "name": val[0],
                    "weight": val[1],
                    "about": paragraph_dict[val[0]]
                } for val in result
            ],
            "message": "ok"
        }
    except:
        reform = {
          "result": [],
          "message": "does not exist"
        }

    return reform



@router.get("/article/parapraph")
async def to_paragraph(
    key: str,
    size: Optional[int] = 25
):
    try:
        result = nlp_core.article_to_paragraph(key, size)
        reform = {
            "result": [
                {
                    "name": val[0],
                    "weight": val[1],
                    "about": paragraph_dict[val[0]]
                } for val in result
            ],
            "message": "ok"
        }

    except:
        reform = {
          "result": [],
          "message": "does not exist"
        }

    return reform\

@router.get("/paragraph/article")
async def to_article(
    key: str,
    size: Optional[int] = 25
):
    try:
        result = nlp_core.paragraph_to_article(key, size)
        reform = {
            "result": [
                {
                    "name": val[0],
                    "weight": val[1],
                    "about": article_dict[val[0]]
                } for val in result
            ],
            "message": "ok"
        }
    except:
        reform = {
          "result": [],
          "message": "does not exist"
        }

    return reform




