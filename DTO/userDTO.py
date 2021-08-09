from typing import List
from pydantic import BaseModel

from .itemDTO import ItemDTO


class UserBaseDTO(BaseModel):
    email: str


class UserCreateDTO(UserBaseDTO):
    password: str
    is_active: bool = True


class UserDTO(UserBaseDTO):
    id: int
    is_active: bool
