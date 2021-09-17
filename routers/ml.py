from fastapi import APIRouter, Query, Depends
from typing import Optional

from lib.DocumentCore import Core
from lib.data_utils import get_paragraph_dict, get_article_dict

from schemas.legacyDatabase import LegacyDatabase

from DTO.userDTO import UserDTO

from routers.auth import current_jwt_validate

db = LegacyDatabase()

router = APIRouter(
    prefix="/ml",
    tags=["ml"],
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
            result = nlp_core.article.search(query, size)
        else:
            result = nlp_core.paragraph.search(query, size)
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
        result = nlp_core.article.article(key, size)
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
        result = nlp_core.paragraph.paragraph(key, size)
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
        result = nlp_core.article.paragraph(key, size)
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


@router.get("/paragraph/article")
async def to_article(
    key: str,
    size: Optional[int] = 25
):
    try:
        result = nlp_core.paragraph.article(key, size)
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


@router.get("/related")
async def log_related(
    current_user: UserDTO = Depends(current_jwt_validate),
):
    query = """SELECT content_type, content_key, created_at FROM view_log WHERE user_id = :user_id ORDER BY created_at DESC LIMIT 10;"""
    params = {
        "user_id": current_user.id
    }

    res = await db.executeAll(query, params)
    return {
        "user" : current_user,
        "result": res
    }
