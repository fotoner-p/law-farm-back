from typing import Optional

from pydantic import BaseModel


class ItemBaseDTO(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBaseDTO):
    pass


class ItemDTO(ItemBaseDTO):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
