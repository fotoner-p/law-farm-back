import datetime

from typing import List
from pydantic import BaseModel


class LogBase(BaseModel):
    content_type: str
    content_key: str


class LogCreate(LogBase):
    text: str
    pass


class LogUpdate(LogBase):
    pass


class Log(LogBase):
    created_at: datetime.datetime
    id: int
    text: str

    class Config:
        orm_mode = True


class LogPage(BaseModel):
    data: List[Log] = []
    count: int
    size: int
    skip: int
    limit: int

