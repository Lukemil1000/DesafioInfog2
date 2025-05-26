import pytest
from cpf_generator import CPF
from sqlalchemy import select

from DesafioInfog2.models import User, Client
from tests.factories import UserFactory, ClientFactory


def test_create_user_in_database(session):
    new_user = UserFactory(username="aaa")
    session.add(new_user)
    session.commit()

    found_user = session.scalar(select(User).where(User.username == "aaa"))

    assert found_user.username == "aaa"

def test_create_client_in_database(session):
    cpf = CPF.format(CPF.generate())
    new_client = ClientFactory(cpf=cpf)
    session.add(new_client)
    session.commit()

    found_client = session.scalar(select(Client).where(Client.cpf == cpf))

    assert found_client.cpf == cpf