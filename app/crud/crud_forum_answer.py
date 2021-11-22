from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import ForumAnswer, User
from app.schemas import ForumAnswerCreate, ForumAnswerUpdate


class CRUDForumAnswer(CRUDBase[ForumAnswer, ForumAnswerCreate, ForumAnswerUpdate]):
    def get_multi_by_forum(self, db: Session, forum_id):
        return db.query(self.model, User).join(User, User.id == self.model.owner_id).filter(self.model.forum_id == forum_id).order_by(self.model.created_at.asc()).all()

    def remove_with_owner_and_id(self, db: Session, *, owner_id: int, obj_id: int, forum_id: int):
        obj = db.query(self.model).filter(self.model.owner_id == owner_id).filter(self.model.id == obj_id).filter(self.model.forum_id == forum_id).first()
        db.delete(obj)
        db.commit()
        return obj


forumAnswer = CRUDForumAnswer(ForumAnswer)
