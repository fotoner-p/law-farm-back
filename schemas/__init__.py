# import os
#
# DB_ENV = {
#     "user": "root",
#     "password": "lawfarm2021",
#     "host": "mysql",
#     "db": "lawfarm",
# } if os.getenv("DEBUG") else {
#     "user": os.getenv("MYSQL_USER"),
#     "password": os.getenv("MYSQL_PASSWORD"),
#     "host": os.getenv("MYSQL_HOST"),
#     "db": os.getenv("MYSQL_DB"),
# }

from .user import User, UserBase, UserCreate
from .token import TokenPayload, Token
from .bookmark import Bookmark, BookmarkBase, BookmarkCreate
from .log import LogBase, LogCreate, Log

