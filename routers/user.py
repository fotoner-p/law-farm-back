from typing import List, Optional
import bcrypt

from fastapi import APIRouter, Form, HTTPException, Depends

from routers.auth import current_jwt_validate
from schemas.database import database
from DTO.userDTO import UserDTO

db = database()

router = APIRouter(
    prefix="/user",
    tags=["user"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.on_event("startup")
async def startup():
    await db.base.connect()


@router.on_event("shutdown")
async def shutdown():
    await db.base.disconnect()


@router.get("/", response_model=List[UserDTO], dependencies=[Depends(current_jwt_validate)])
async def read_all_users():
    query = """SELECT * FROM user;"""
    res = await db.executeAll(query)

    return res


@router.get("/bookmark")
async def get_bookmark(
        current_user: UserDTO = Depends(current_jwt_validate),
):
    query = """SELECT content_type, content_key, created_at FROM bookmark WHERE user_id = :user_id ORDER BY created_at DESC;"""
    params = {
        "user_id": current_user.id
    }

    res = await db.executeAll(query, params)
    return {
        "user" : current_user,
        "result": res
    }


@router.post("/bookmark")
async def add_bookmark(
        current_user: UserDTO = Depends(current_jwt_validate),
        key: str = Form(...),
        content_type: str = Form(..., regex="(article|paragraph)")
):
    check_query = """SELECT content_type, content_key, created_at FROM bookmark WHERE user_id = :user_id AND content_key = :content_key AND content_type = :content_type;"""
    params = {
        "user_id": current_user.id,
        "content_type": content_type,
        "content_key": key
    }

    res = await db.executeOne(check_query, params)

    if res:
        return {
            "item": params,
            "result": "fail",
            "message": "already exists"
        }

    add_query = """INSERT INTO bookmark(user_id, content_type, content_key, created_at) VALUES(:user_id, :content_type, :content_key, NOW());"""

    try:
        await db.execute(add_query, params)

        return {
            "user": current_user,
            "result": "ok"
        }

    except Exception as e:
        return {
            "message": e,
            "user": current_user,
            "result": "fail"
        }


@router.delete("/bookmark")
async def remove_bookmark(
    current_user: UserDTO = Depends(current_jwt_validate),
    key: str = Form(...),
    content_type: str = Form(..., regex="(article|paragraph)")
):
    query = """DELETE FROM bookmark WHERE user_id = :user_id AND content_key = :content_key AND content_type = :content_type; """
    params = {
        "user_id": current_user.id,
        "content_type": content_type,
        "content_key": key
    }

    try:
        await db.execute(query, params)

        return {
            "user": current_user,
            "result": "ok"
        }

    except Exception as e:
        return {
            "message": e,
            "user": current_user,
            "result": "fail"
        }


@router.get("/log")
async def get_view_log(
        current_user: UserDTO = Depends(current_jwt_validate)
):
    query = """SELECT content_type, content_key, created_at FROM view_log WHERE user_id = :user_id ORDER BY created_at DESC;"""
    params = {
        "user_id": current_user.id
    }

    res = await db.executeAll(query, params)
    return {
        "user": current_user,
        "result": res
    }