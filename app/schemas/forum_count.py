from pydantic import BaseModel


class ForumCountBase(BaseModel):
    pass


class ForumCountCreate(ForumCountBase):
    forum_id: int
    owner_id: int


class ForumCountUpdate(ForumCountCreate):
    pass
