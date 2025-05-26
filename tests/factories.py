import factory
from cpf_generator import CPF

from DesafioInfog2.models import User, Client


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}_password')

class ClientFactory(factory.Factory):
    class Meta:
        model = Client

    name = factory.sequence(lambda n: f"client{n}")
    email = factory.LazyAttribute(lambda obj: f'{obj.name}@test.com')
    cpf = CPF.format(CPF.generate())