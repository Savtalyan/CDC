from factories.post_factory import PostFactory
from factories.user_factory import UserFactory


class DataFactory:
    user_factory = UserFactory
    post_factory = PostFactory

    @staticmethod
    def generate(users_n, posts_n):
        users = DataFactory.user_factory.create_many(users_n)
        users_ids = list(range(1, users_n + 1))

        posts = DataFactory.post_factory.create_many(users_ids, posts_n)

        return users, posts
