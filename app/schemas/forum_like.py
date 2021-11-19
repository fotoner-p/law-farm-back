import datetime

from pydantic import BaseModel


class ForumLikeBase(BaseModel):
    pass


class ForumLikeCreate(ForumLikeBase):
    forum_id: int
    owner_id: int


class ForumLikeUpdate(ForumLikeBase):
    pass


class ForumLikeDB(ForumLikeBase):
    created_at: datetime.datetime
    id: int

    class Config:
        orm_mode = True


class ForumLike(ForumLikeDB):
    pass
