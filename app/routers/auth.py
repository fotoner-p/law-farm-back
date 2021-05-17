# from fastapi import status, HTTPException, Depends, APIRouter, Form
# from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
#
# from typing import Optional
# from pydantic import BaseModel
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
#
# import bcrypt
#
# from ..DTO.userDTO import UserDTO
# from ..schemas.models import get_user, get_bucket, User
#
# SECRET_KEY = "tomuchsecret"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
#
# class Token(BaseModel):
#     access_token: str
#     token_type: str
#     email: str
#
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
# router = APIRouter(
#     prefix="/auth",
#     tags=["auth"],
#     # dependencies=[Depends(get_token_header)],
#     responses={404: {"description": "Not found"}},
# )
#
#
# @router.on_event("startup")
# async def startup():
#     await database.connect()
#
#
# @router.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()
#
#
# async def current_jwt_validate(token: str = Depends(oauth2_scheme)) -> UserDTO:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: str = payload.get("id")
#         expire: int = payload.get("exp")
#
#         if user_id is None:
#             raise credentials_exception
#         elif expire < datetime.utcnow().timestamp():
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#
#     sql = "SELECT id, email, is_active FROM users WHERE id = :id;"
#     params = {
#         "id": user_id
#     }
#     res = await database.fetch_one(sql, params)
#
#     if not res:
#         raise credentials_exception
#     else:
#         return UserDTO(id=res['id'], email=res['email'], is_active=res['is_active'])
#
#
# async def authenticate_user(email: str, password: str):
#     sql = "SELECT id, email, is_active, hashed_password FROM users WHERE email = :email;"
#     params = {
#         "email": email
#     }
#
#     res = await database.fetch_one(sql, params)
#
#     if res:
#         if bcrypt.checkpw(password.encode('utf-8'), res['hashed_password'].encode('utf-8')):
#             return UserDTO(id=res['id'], email=res['email'], is_active=res['is_active'])
#     return False
#
#
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# @router.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await authenticate_user(form_data.username, form_data.password)
#
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"id": user.id, "email": user.email},
#         expires_delta=access_token_expires
#     )
#
#     return {"access_token": access_token, "token_type": "bearer", "id": user.id, "email": user.email}
