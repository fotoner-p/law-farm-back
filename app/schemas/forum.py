import datetime

from typing import Optional
from pydantic import BaseModel


class ForumBase(BaseModel):
    pass


class ForumDbBase(ForumBase):
    title: str
    forum_type: str


class ForumCreate(ForumBase):
    title: str
    forum_type: str
    main: str
    secret: bool


class ForumUpdate(ForumBase):
    title: Optional[str] = None
    forum_type: Optional[str] = None
    main: Optional[str] = None


class ForumDB(ForumDbBase):
    created_at: datetime.datetime
    id: int
    owner_id: int
    secret: bool
    like_count: int
    comment_count: int
    view_count: int

    class Config:
        orm_mode = True


class Forum(ForumDB):
    main: str


class ForumList(ForumDB):
    parse_short_main: str