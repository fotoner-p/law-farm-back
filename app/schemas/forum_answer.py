import datetime

from typing import List
from pydantic import BaseModel
from .user import User


class ForumAnswerBase(BaseModel):
    pass


class ForumAnswerDbBase(ForumAnswerBase):
    main: str


class ForumAnswerCreate(ForumAnswerDbBase):
    owner_id: int
    forum_id: int


class ForumAnswerUpdate(ForumAnswerDbBase):
    pass


class ForumAnswerDB(ForumAnswerDbBase):
    id: int
    forum_id: int
    owner_id: int
    created_at: datetime.datetime
    # like_count: int

    class Config:
        orm_mode = True


class ForumAnswer(ForumAnswerDB):
    pass


class ForumAnswerUser(ForumAnswer):
    user: User


class ForumAnswerPage(BaseModel):
    data: List[ForumAnswerUser] = []
