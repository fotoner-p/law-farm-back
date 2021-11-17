import datetime

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base

# 나중에 방법 알고 쪼개기


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(99), unique=True, index=True, nullable=False)
    hashed_password = Column(String(99), nullable=False)
    username = Column(String(30), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    bookmarks = relationship("Bookmark", back_populates="owner")
    view_logs = relationship("ViewLog", back_populates="owner")
    forums = relationship("Forum", back_populates="owner")
    forum_counts = relationship("ForumCount", back_populates="owner")
    forum_likes = relationship("ForumLike", back_populates="owner")
    forum_answers = relationship("ForumAnswer", back_populates="owner")
    forum_answer_likes = relationship("ForumAnswerLike", back_populates="owner")
    forum_answer_comments = relationship("ForumAnswerComment", back_populates="owner")


class Bookmark(Base):
    __tablename__ = 'bookmarks'

    id = Column(Integer, primary_key=True, index=True)
    content_type = Column(String(15), nullable=False)
    content_key = Column(String(99), nullable=False)
    text = Column(String(99), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="bookmarks")


class ViewLog(Base):
    __tablename__ = 'view_logs'

    id = Column(Integer, primary_key=True, index=True)
    content_type = Column(String(15), nullable=False)
    content_key = Column(String(99), nullable=False)
    text = Column(String(99), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="view_logs")


class Forum(Base):
    __tablename__ = 'forum'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(30), index=True, nullable=False)
    secret = Column(Boolean(), nullable=False, default=False)
    forum_type = Column(String(99), nullable=False)
    main = Column(Text(4294000000), nullable=False, default='')
    parse_short_main = Column(Text(4294000000), nullable=False, default='')
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    like_count = Column(Integer, nullable=False, default=0)
    view_count = Column(Integer, nullable=False, default=0)
    comment_count = Column(Integer, nullable=False, default=0)

    owner = relationship("User", back_populates="forums")

    counts = relationship("ForumCount", back_populates="forum_owner")
    likes = relationship("ForumLike", back_populates="forum_owner")
    answers = relationship("ForumAnswer", back_populates="forum_owner")


class ForumCount(Base):
    __tablename__ = 'forum_count'

    id = Column(Integer, primary_key=True, index=True)
    forum_id = Column(Integer, ForeignKey("forum.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="forum_counts")
    forum_owner = relationship("Forum", back_populates="counts")


class ForumLike(Base):
    __tablename__ = 'forum_like'

    id = Column(Integer, primary_key=True, index=True)
    forum_id = Column(Integer, ForeignKey("forum.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    is_like = Column(Boolean(), nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="forum_likes")
    forum_owner = relationship("Forum", back_populates="likes")


class ForumAnswer(Base):
    __tablename__ = 'forum_answer'

    id = Column(Integer, primary_key=True, index=True)
    forum_id = Column(Integer, ForeignKey("forum.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    main = Column(Text(4294000000), nullable=False, default='')
    like_count = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="forum_answers")
    forum_owner = relationship("Forum", back_populates="answers")

    answer_likes = relationship("ForumAnswerLike", back_populates="answer_owner")
    answer_comments = relationship("ForumAnswerComment", back_populates="answer_owner")


class ForumAnswerLike(Base):
    __tablename__ = 'forum_answer_like'

    id = Column(Integer, primary_key=True, index=True)
    answer_id = Column(Integer, ForeignKey("forum_answer.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    is_like = Column(Boolean(), nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="forum_answer_likes")
    answer_owner = relationship("ForumAnswer", back_populates="answer_likes")


class ForumAnswerComment(Base):
    __tablename__ = 'forum_answer_comment'

    id = Column(Integer, primary_key=True, index=True)
    answer_id = Column(Integer, ForeignKey("forum_answer.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    main = Column(Text(), nullable=False, default='')

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="forum_answer_comments")
    answer_owner = relationship("ForumAnswer", back_populates="answer_comments")


