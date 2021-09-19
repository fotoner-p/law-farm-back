import datetime

from pydantic import BaseModel


class BookmarkBase(BaseModel):
    content_type: str
    content_key: str


class BookmarkCreate(BookmarkBase):
    pass


class Bookmark(BookmarkBase):
    created_at: datetime.datetime

    class Config:
        orm_mode = True

