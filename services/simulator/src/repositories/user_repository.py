from sqlalchemy import update, delete, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models import User

class UserRepository:

    def __init__(self, session):
        self.session = session

    def insert(self, data: dict) -> int | None:
        stmt = insert(User).values(**data).on_conflict_do_nothing().returning(User.id)
        user_id = self.session.scalar(stmt)
        self.session.commit()
        return user_id

    def random_user(self) -> int | None:
        return self.session.scalar(select(User.id).order_by(func.random()).limit(1))

    def count(self) -> int:
        return self.session.scalar(select(func.count()).select_from(User))

    def delete(self, user_id) -> None:
       self.session.execute(delete(User).where(User.id == user_id))
       self.session.commit()

    def update(self, user_id: int, **fields) -> None:
        self.session.execute(update(User).where(User.id == user_id).values(**fields))
        self.session.commit()
