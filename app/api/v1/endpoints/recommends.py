from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional, Any

from app.lib.DocumentCore import Core
from app.lib.data_utils import get_paragraph_dict, get_article_dict, get_statues_dict

from sqlalchemy.orm import Session
import app.api.dependency as deps

from app import crud, schemas, models

router = APIRouter(
    prefix="/recommends",
    tags=["recommends"],
    responses={404: {"description": "Not found"}},
)

nlp_core = Core()
paragraph_dict: dict = get_paragraph_dict()
article_dict: dict = get_article_dict()
statute_dict: dict = get_statues_dict()

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


def query_wrapper(*, callback, query, size: int):
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


@router.get("/statute/inference")
async def inference_type(
        query: str,
        size: Optional[int] = SIZE_OPTION_DEFAULT
) -> Any:
    result = query_wrapper(
        callback=nlp_core.statute.inference_statute,
        query=query,
        size=size
    )

    return {
        "result": [
            {
                "name": val[0],
                "weight": val[1],
            } for val in result
        ],
        "detail": "ok"
    }


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


@router.get("/log/article")
async def get_log_bass_article_recommends(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        size: Optional[int] = SIZE_OPTION_DEFAULT,
        duplicate: Optional[bool] = False
) -> Any:
    logs = crud.log.get_multi_by_owner(db, owner=current_user, skip=0, limit=100)
    documents = [log.content_key for log in logs]

    if len(documents) == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    try:
        result = nlp_core.article.recommend(documents, size, duplicate)
    except:
        raise HTTPException(status_code=404, detail="Item not found")

    return reform_result(result, article_dict)


@router.get("/log/statute")
async def get_log_bass_statute_recommends(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        size: Optional[int] = SIZE_OPTION_DEFAULT
) -> Any:
    logs = crud.log.get_multi_by_owner(db, owner=current_user, skip=0, limit=100)
    documents = [log.content_key for log in logs]

    if len(documents) == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    try:
        result = nlp_core.statute.recommend(documents, size, False)
    except:
        raise HTTPException(status_code=404, detail="Item not found")

    return {
        "result": [
            {
                "name": val[0],
                "weight": val[1],
            } for val in result
        ],
        "detail": "ok"
    }


@router.get("/bookmark/article")
async def get_bookmark_bass_article_recommends(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        size: Optional[int] = SIZE_OPTION_DEFAULT,
        duplicate: Optional[bool] = False
) -> Any:
    bookmarks = crud.bookmark.get_multi_by_owner(db, owner=current_user, skip=0, limit=100)
    documents = [bookmark.content_key for bookmark in bookmarks]

    try:
        result = nlp_core.article.recommend(documents, size, duplicate)
    except:
        raise HTTPException(status_code=404, detail="Item not found")

    return reform_result(result, article_dict)


@router.get("/combined/article")
async def get_combined_bass_article_recommends(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        size: Optional[int] = SIZE_OPTION_DEFAULT,
        duplicate: Optional[bool] = False
) -> Any:
    bookmarks = crud.bookmark.get_multi_by_owner(db, owner=current_user, skip=0, limit=100)
    bookmark_article = [bookmark.content_key for bookmark in bookmarks]

    logs = crud.log.get_multi_by_owner(db, owner=current_user, skip=0, limit=100)
    log_article = [log.content_key for log in logs]

    if len(bookmark_article) == 0 or len(log_article) == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    documents = {
        "log": log_article,
        "bookmark": bookmark_article
    }

    try:
        result = nlp_core.article.combined_recommend(documents, size, duplicate)
    except:
        raise HTTPException(status_code=404, detail="Item not found")

    return reform_result(result, article_dict)

