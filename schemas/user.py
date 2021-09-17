from typing import List
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    is_active: bool = True


class User(UserBase):
    id: int
    is_active: bool

