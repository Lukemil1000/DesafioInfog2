from jwt import decode

from DesafioInfog2.security import create_access_token, settings


def test_create_access_token():
    data = {"sub": "test"}
    token = create_access_token(data=data)
    decoded = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert decoded['sub'] == data['sub']
    assert decoded['exp']