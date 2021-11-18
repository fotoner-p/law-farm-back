from pydantic import BaseModel


class ForumLikeBase(BaseModel):
    pass


class ForumLikeCreate(ForumLikeBase):
    forum_id: int
    owner_id: int


class ForumLikeUpdate(ForumLikeBase):
    pass
