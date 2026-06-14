from faker import Faker

fake = Faker()

class UserFactory:
    @staticmethod
    def create():
        return {
            "u_first_name" : fake.first_name(),
            "u_last_name"  : fake.last_name(),
            "u_email"  : fake.email(),
            "u_phone" : fake.phone(),
            "u_city" : fake.city(),
            "u_country" : fake.country(),
            "u_postal" : fake.postal()
        }
    
    @staticmethod
    def create_many(n):
        return (UserFactory.create() for _ in range(n))