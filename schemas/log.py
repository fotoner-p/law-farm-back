import datetime

from pydantic import BaseModel


class LogBase(BaseModel):
    content_type: str
    content_key: str


class LogCreate(LogBase):
    pass


class Log(LogBase):
    created_at: datetime.datetime
    id: int

    class Config:
        orm_mode = True
