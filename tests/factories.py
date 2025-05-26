import factory
import factory.fuzzy
from cpf_generator import CPF

from DesafioInfog2.models import User, Client, Product, Order, OrderState


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}_password')

class ClientFactory(factory.Factory):
    class Meta:
        model = Client

    name = factory.Faker("first_name")
    email = factory.LazyAttribute(lambda obj: f'{obj.name}@test.com')
    cpf = CPF.format(CPF.generate())

class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    name = factory.Faker("first_name")
    description = factory.Faker("sentence")
    price = factory.Faker("pyfloat", min_value=1.0)
    category = factory.Faker("word")
    stock = factory.Faker("pyint", min_value=0)
    expire_date = factory.Faker("date_time_this_year", before_now=False, after_now=True)

class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    state = factory.fuzzy.FuzzyChoice(OrderState)
    products = [ProductFactory()]
    client_id = 1