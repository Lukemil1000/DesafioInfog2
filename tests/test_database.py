import pytest
from sqlalchemy import select

from DesafioInfog2.models import User
from tests.factories import UserFactory


def test_create_user_in_database(session):
    new_user = UserFactory(username="aaa")
    session.add(new_user)
    session.commit()

    found_user = session.scalar(select(User).where(User.username == "aaa"))

    assert found_user.username == "aaa"