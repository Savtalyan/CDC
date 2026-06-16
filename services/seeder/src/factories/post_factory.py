from faker import Faker
import random

fake = Faker()


class PostFactory:

    @staticmethod
    def create(user_ids):
        return {
            "user_id": random.choice(user_ids),
            "title": fake.sentence(nb_words=5),
            "content": fake.text(max_nb_chars=200),
        }

    @staticmethod
    def create_many(user_ids, n):
        return [PostFactory.create(user_ids) for _ in range(n)]
