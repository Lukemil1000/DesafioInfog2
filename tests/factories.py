import factory

from DesafioInfog2.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}_password')