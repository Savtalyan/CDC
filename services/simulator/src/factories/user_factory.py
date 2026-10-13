from faker import Faker

fake = Faker()


class UserFactory:
    @staticmethod
    def create():
        return {
            "u_first_name": fake.first_name(),
            "u_last_name": fake.last_name(),
            "u_email": fake.email(),
            "u_phone": fake.phone_number(),
            "u_city": fake.city(),
            "u_country": fake.country(),
            "u_postal": fake.postcode(),
        }

    @staticmethod
    def create_many(n):
        return [UserFactory.create() for _ in range(n)]

    @staticmethod
    def create_email():
        return fake.email()

    @staticmethod
    def create_phone():
        return fake.phone_number()

    @staticmethod
    def create_city():
        return fake.city()

    @staticmethod
    def create_country():
        return fake.country()

    @staticmethod
    def create_postal_code():
        return fake.postcode()
