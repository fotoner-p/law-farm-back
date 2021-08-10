from fastapi import status, HTTPException, Depends, APIRouter, Form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from typing import Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt

import bcrypt
import os

from DTO.userDTO import UserDTO
from schemas.database import database

db = database()

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str
    email: str
    id: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.on_event("startup")
async def startup():
    await db.base.connect()


@router.on_event("shutdown")
async def shutdown():
    await db.base.disconnect()


async def current_user_state(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        expire: int = payload.get("exp")

        if user_id is None:
            return {
                "login": False
            }
        elif expire < datetime.utcnow().timestamp():
            return {
                "login": False
            }

    except JWTError:
        return {
            "login": False
        }

    sql = "SELECT id, email, is_active FROM user WHERE id = :id;"
    params = {
        "id": user_id
    }

    res = await db.executeOne(sql, params)

    if not res:
        return {
            "login": False
        }
    else:
        return {
            "login": True,
            "user": UserDTO(id=res['id'], email=res['email'], is_active=res['is_active'])
        }


async def current_jwt_validate(token: str = Depends(oauth2_scheme)) -> UserDTO:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        expire: int = payload.get("exp")

        if user_id is None:
            raise credentials_exception
        elif expire < datetime.utcnow().timestamp():
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    sql = "SELECT id, email, is_active FROM user WHERE id = :id;"
    params = {
        "id": user_id
    }

    res = await db.executeOne(sql, params)

    if not res:
        raise credentials_exception
    else:
        return UserDTO(id=res['id'], email=res['email'], is_active=res['is_active'])


async def authenticate_user(email: str, password: str):
    sql = "SELECT id, email, is_active, password FROM user WHERE email = :email;"
    params = {
        "email": email
    }

    res = await db.executeOne(sql, params)

    if res:
        if bcrypt.checkpw(password.encode('utf-8'), res['password'].encode('utf-8')):
            return UserDTO(id=res['id'], email=res['email'], is_active=res['is_active'])
    return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60 * 4)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/register')
async def register(
        email: str = Form(..., regex='^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$'),
        username: str = Form(..., min_length=3, max_length=20),
        password: str = Form(..., min_length=10, max_length=72),
):
    check_user_sql ="SELECT email, username FROM user WHERE email = :email;"
    email_res = await db.executeAll(check_user_sql, {"email": email})

    if len(email_res) > 0:
        raise HTTPException(status_code=400, detail="email already exist (email: %s)" % email)

    check_user_sql ="SELECT email, username FROM user WHERE username = :username"
    username_res = await db.executeAll(check_user_sql, {"username": username})

    if len(username_res) > 0:
        raise HTTPException(status_code=400, detail="user already exist (usename: %s)" % username)

    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    create_sql = "INSERT INTO user (email, username, password, created_at) VALUES(:email, :username, :password, NOW());"

    await db.execute(create_sql, {"email": email, "username": username, "password": hashed_pwd})

    return {
        "username": username,
        "status": "created"
    }


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": user.id, "email": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "id": user.id, "email": user.email}
