from typing import List

import datetime

from pydantic import BaseModel


class BookmarkBase(BaseModel):
    content_type: str
    content_key: str


class BookmarkCreate(BookmarkBase):
    text: str


class BookmarkUpdate(BookmarkBase):
    pass


class Bookmark(BookmarkBase):
    created_at: datetime.datetime
    id: int
    text: str
    owner_id: int
    
    class Config:
        orm_mode = True


class BookmarkPage(BaseModel):
    data: List[Bookmark] = []
    count: int
    size: int
    skip: int
    limit: int

