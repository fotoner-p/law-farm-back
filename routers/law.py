from typing import Optional

from fastapi import APIRouter, Depends
from lib.data_utils import get_paragraph_dict, get_article_dict
from routers.auth import current_jwt_validate
from schemas.database import database
from DTO.userDTO import UserDTO

db = database()

router = APIRouter(
    prefix="/law",
    tags=["law"],
    responses={404: {"description": "Not found"}},
)

paragraph_dict: dict = get_paragraph_dict()
article_dict: dict = get_article_dict()
article_names = sorted([key for key in article_dict.keys()])


@router.on_event("startup")
async def startup():
    await db.base.connect()


@router.on_event("shutdown")
async def shutdown():
    await db.base.disconnect()


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


@router.get("/article/log")
async def get_article(
        key: str,
        current_user: UserDTO = Depends(current_jwt_validate),
):
    try:
        result = article_dict[key]

        query = """INSERT INTO view_log (user_id, content_key, content_type, created_at) VALUES(:user_id, :content_key, :content_type, NOW());"""
        params = {
            "user_id": current_user.id,
            "content_key": key,
            "content_type": "article"
        }

        await db.execute(query, params)

        return {
            "result": result,
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


@router.get("/paragraph/log")
async def get_paragraph(
        key: str,
        current_user: UserDTO = Depends(current_jwt_validate),
):
    try:
        result = paragraph_dict[key]

        query = """INSERT INTO view_log (user_id, content_key, content_type, created_at) VALUES(:user_id, :content_key, :content_type, NOW());"""
        params = {
            "user_id": current_user.id,
            "content_key": key,
            "content_type": "paragraph"
        }

        await db.execute(query, params)

        return {
            "result": result,
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
