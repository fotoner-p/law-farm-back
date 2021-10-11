import datetime

from typing import List
from pydantic import BaseModel


class LogBase(BaseModel):
    content_type: str
    content_key: str


class LogCreate(LogBase):
    pass


class LogUpdate(LogBase):
    pass


class Log(LogBase):
    created_at: datetime.datetime
    id: int

    class Config:
        orm_mode = True


class LogPage(BaseModel):
    data: List[Log] = []
    count: int
    size: int
    skip: int
    limit: int

