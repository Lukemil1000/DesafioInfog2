import pytest
from sqlalchemy import select

from DesafioInfog2.models import User


def test_create_user_in_database(session):
    new_user = User(username="test", email="test@test.com", password="test_password")
    session.add(new_user)
    session.commit()

    found_user = session.scalar(select(User).where(User.username == "test"))

    assert found_user.username == "test"