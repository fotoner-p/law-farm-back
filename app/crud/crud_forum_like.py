from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import ForumLike
from app.schemas import ForumLikeCreate, ForumLikeUpdate


class CRUDForumLike(CRUDBase[ForumLike, ForumLikeCreate, ForumLikeUpdate]):
    def get_with_owner_and_forum(self, db: Session, *, forum_id: int, owner_id: int):
        return db.query(self.model).filter(self.model.owner_id == owner_id).filter(self.model.forum_id ==forum_id).first()


forumLike = CRUDForumLike(ForumLike)
