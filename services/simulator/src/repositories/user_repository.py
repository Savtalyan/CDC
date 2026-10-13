
from simulator.factories.user_factory import UserFactory
from sqlalchemy.orm import Session

class UserRepository:

    def __init__(self, session):
        self.session = session

    def insert(self) -> int | None:
        user = UserFactory.create()

        stmt = insert(User).values(**user).on_failure_do_nothing().returning(User.id)
        user_id = self.session.scalar(stmt)
        self.session.commit()
        return user_id

    def random_user(self) -> int | None:
        return self.session.scalar(select(User.id).order_by(func.random()).limit(1))

    def count(self) -> int:
        return self.session.scalar(select(func.count())).select_from(User)

    def delete(self) -> None:
       user_id = self.random_id()
       self.session.execute(delete(User).where(User.id = user_id))
       self.session.commit()

    def update(self, user_id: int, **fields) -> None:
        self.session.execute(update(User).where(User.id == user_id).values(**fields))
        self.session.commit()
