from typing import List, Optional
import bcrypt

from fastapi import APIRouter, Form, HTTPException, Depends

from .auth import current_jwt_validate
from ..schemas.database import database
from ..DTO.userDTO import UserDTO, UserCreateDTO

database = database()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.on_event("startup")
async def startup():
    await database.connect()


@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@router.get("/", response_model=List[UserDTO], dependencies=[Depends(current_jwt_validate)])
async def read_all_users():
    query = """SELECT id, email, is_active FROM users;"""
    res = await database.fetch_all(query)

    return res


@router.post("/")
async def create_new_user(
        email: str = Form(...), #, min_length=3, max_length=20),
        password: str = Form(..., min_length=10, max_length=72),
        is_active: Optional[bool] = Form(None)
):
    is_active = is_active if is_active is not None else True

    check_user_sql ="""SELECT email FROM users WHERE email=:email;"""

    params = {
        "email": email
    }
    query_res = await database.fetch_one(check_user_sql, params)

    if query_res:
        raise HTTPException(status_code=400, detail=f"user already exist (user: {email})")

    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    create_sql = """INSERT INTO users(email, hashed_password, is_active) VALUES(:email, :hashed_password, :is_active)"""

    params = {
        "email": email,
        "hashed_password": hashed_pwd,
        "is_active": is_active,
    }

    last_record_id = await database.execute(create_sql, params)
    print(last_record_id)
    user = UserDTO(
        id=last_record_id,
        email=email,
        is_active=is_active
    )

    return {**user.dict()}


