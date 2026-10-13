
from simulator.factories.post_factory import PostFactory
from sqlalchemy.orm import Session

class PostRepository:
    def __init__(self, session):
        self.session = session

    def insert(self) -> int | None:
        post = PostFactory.create()
        stmt = insert(Post).values(**post).on_conflict_do_nothing().returning(Post.id)
        post_id = self.session.scalar(stmt)
        self.session.commit()
        return post_id
    
    def random_id(self) -> int | None:
        return self.session.scalar(select(Post.id).order_by(func.random()).limit(1))
    
    def count(self) -> int | None:
        return self.session.scalar(select(func.count()).select_from(Post))

    def delete(self) -> None:
        post_id = self.random_id()

        self.session.execute(delete(Post).where(Post.id = post_id))
        self.session.commit()
   
    def update(self, post_id: int, **fields) -> None:
        self.session.execute(update(Post).where(Post.id == post_id).values(**fields))
        self.session.commit()
