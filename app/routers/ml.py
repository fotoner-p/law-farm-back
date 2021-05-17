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

nlpCore = Core()
parameter_dict: dict = get_paragraph_dict()
article_dict: dict = get_article_dict()


@router.get("/search")
async def read_all_users(
    query: str,
    target: str = Query("article", regex="(statute|article|paragraph|)"),
    size: Optional[int] = 25
):
    if target == "article":
        result = nlpCore.search_article(query, size)
        reform = {
            "result": [
                {
                    "name": val[0],
                    "weight": val[1],
                    "about": article_dict[val[0]]
                } for val in result
            ]
        }

    else:
        result = nlpCore.search_paragraph(query, size)
        reform = {
            "result": [
                {
                    "name": val[0],
                    "weight": val[1],
                    "about": parameter_dict[val[0]]
                } for val in result
            ]
        }

    return reform
